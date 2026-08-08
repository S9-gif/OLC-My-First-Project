import feedparser
import requests
import time
from time import mktime
import re
from datetime import datetime
from config import BACKEND_URL, RSS_FEEDS


def clean_html(raw_html):
    """HTML tag'lerini temizle"""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]*>', '', raw_html)
    return clean.strip()

def get_published_date(entry):
    """RSS entry'den ISO 8601 formatında tarih çıkar"""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime.fromtimestamp(mktime(entry.published_parsed))
        return dt.isoformat()
    return datetime.utcnow().isoformat()

def get_full_text(entry):
    """RSS entry'den tam metni çıkar (content, content:encoded, summary sırasıyla dene)"""
    if hasattr(entry, "content") and entry.content:
        return entry.content[0].value
    if hasattr(entry, "summary"):
        return entry.summary
    return ""


def fetch_feed(feed_config):
    """Tek bir RSS feed'i çek ve haber listesi döndür"""
    url = feed_config["url"]
    kategori = feed_config["kategori"]
    kaynak_adi = feed_config["kaynak_adi"]

    print(f"📡 Çekiliyor: {kaynak_adi} ({url})")

    try:
        parsed = feedparser.parse(url)
    except Exception as e:
        print(f"❌ Feed okunamadı: {kaynak_adi} - {e}")
        return []

    haberler = []
    for entry in parsed.entries:
        tam_metin = clean_html(get_full_text(entry))

        haber = {
            "baslik": entry.get("title", "Başlık Yok"),
            "kategori": kategori,
            "kaynak_adi": kaynak_adi,
            "kaynak_url": entry.get("link", ""),
            "tam_metin": tam_metin or "Metin yok",
            "yayin_tarihi": get_published_date(entry)

        }
        haberler.append(haber)

    print(f"✅ {len(haberler)} haber bulundu: {kaynak_adi}")
    return haberler


def send_to_backend(haber, max_retries=3):
    """Tek haberi backend'e POST et (retry mekanizmalı)"""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(
                f"{BACKEND_URL}/haberler",
                json=haber,
                timeout=20
            )
            if response.status_code == 201:
                haber_id = response.json().get("id")
                print(f"  ✅ Eklendi (ID: {haber_id}): {haber['baslik'][:50]}...")
                return haber_id
            elif response.status_code == 500 and attempt < max_retries:
                print(f"  ⏳ Backend uyanıyor olabilir, {attempt}. deneme başarısız, 10sn bekleniyor...")
                time.sleep(10)
                continue
            else:
                print(f"  ⚠️ Hata ({response.status_code}): {haber['baslik'][:50]}...")
                return None
        except Exception as e:
            if attempt < max_retries:
                print(f"  ⏳ Bağlantı hatası, {attempt}. deneme, 10sn bekleniyor... ({e})")
                time.sleep(10)
                continue
            print(f"  ❌ Bağlantı hatası (son deneme): {e}")
            return None
    return None

def trigger_ai_processing(haber_id):
    """Backend'de AI işlemeyi tetikle"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/ai/process/{haber_id}",
            timeout=30
        )
        if response.status_code == 200:
            print(f"  🤖 AI işlendi (ID: {haber_id})")
        else:
            print(f"  ⚠️ AI işleme hatası (ID: {haber_id})")
    except Exception as e:
        print(f"  ❌ AI işleme bağlantı hatası: {e}")


def run_all_feeds():
    """Tüm RSS feed'leri çek, backend'e gönder, AI ile işle"""
    print(f"\n{'='*50}")
    print(f"🔄 Otomasyon başladı: {datetime.now()}")
    print(f"{'='*50}\n")

    total_added = 0

    for feed_config in RSS_FEEDS:
        haberler = fetch_feed(feed_config)

        for haber in haberler:
            haber_id = send_to_backend(haber)
            if haber_id:
                trigger_ai_processing(haber_id)
                total_added += 1

    print(f"\n{'='*50}")
    print(f"🎉 Tamamlandı! Toplam {total_added} haber eklendi.")
    print(f"{'='*50}\n")
