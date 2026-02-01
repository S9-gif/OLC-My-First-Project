import streamlit as st
import requests
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="OLC - Open Learn Close",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    /* Ana container */
    .main {
        padding-top: 2rem;
    }

    /* Başlık stilleri */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    h3 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 1rem;
    }

    /* Haber kartları için divider */
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border: none;
        border-top: 2px solid #e0e0e0;
    }

    /* Info box'lar */
    .stAlert > div {
        padding: 1rem;
        border-radius: 0.5rem;
    }

    /* Expander başlıkları */
    .streamlit-expanderHeader {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
    }

    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Metrikler */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }

    /* Butonlar */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Sentiment renkleri */
    .sentiment-positive {
        color: #2ecc71;
        font-weight: 600;
    }

    .sentiment-neutral {
        color: #95a5a6;
        font-weight: 600;
    }

    .sentiment-negative {
        color: #e74c3c;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "https://olc-backend.onrender.com/api/v1"

# Sentiment emoji mapping
SENTIMENT_EMOJI = {
    "olumlu": "😊",
    "nötr": "😐",
    "olumsuz": "😔"
}

# Kategori emoji mapping
KATEGORI_EMOJI = {
    "spor": "⚽",
    "teknoloji": "💻",
    "borsa": "💰",
    "kitap": "📚"
}

# Haber kartı göster (OLC 3-Level)
def show_haber_card(haber):
    sentiment = haber.get('sentiment_label', 'nötr')
    kategori = haber.get('kategori', 'genel')

    with st.container():
        st.markdown(f"### 📰 {haber['baslik']}")

        emoji_sentiment = SENTIMENT_EMOJI.get(sentiment, "😐")
        emoji_kategori = KATEGORI_EMOJI.get(kategori, "📰")

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"{emoji_sentiment} **{sentiment.upper()}**")
        with col2:
            st.markdown(f"{emoji_kategori} **{kategori.upper()}**")
        with col3:
            st.markdown(f"🆔 ID: {haber['id']}")

        st.markdown("#### 📰 OPEN - Hızlı Bakış")
        flash_ozet = haber.get('flash_ozet', 'Özet henüz oluşturulmadı')
        st.info(flash_ozet)

        with st.expander("📚 LEARN - Detaylı Özet"):
            detayli_ozet = haber.get('detayli_ozet', 'Detaylı özet henüz oluşturulmadı')
            if detayli_ozet:
                lines = detayli_ozet.split('\n')
                for line in lines:
                    if line.strip():
                        st.markdown(line)
            else:
                st.warning("Detaylı özet henüz hazır değil")

        with st.expander("📄 CLOSE - Tam Metin & Kaynak"):
            tam_metin = haber.get('tam_metin', 'Tam metin bulunamadı')
            st.markdown(tam_metin)

            st.divider()

            kaynak_url = haber.get('kaynak_url', '#')
            kaynak_adi = haber.get('kaynak_adi', 'Kaynak')
            st.markdown(f"**📰 Kaynak:** [{kaynak_adi}]({kaynak_url})")

            keywords = haber.get('anahtar_kelimeler', [])
            if keywords:
                st.markdown("**🔑 Anahtar Kelimeler:**")
                keyword_tags = " ".join([f"`{k}`" for k in keywords[:5]])
                st.markdown(keyword_tags)

        st.divider()

# Başlık
st.markdown("""
# 📰 OLC - Open Learn Close
### *Üç Seviyeli Haber Okuma Deneyimi*

**Open** (5 sn) → **Learn** (30 sn) → **Close** (2 dk)
""")

# OLC Açıklama
with st.expander("ℹ️ OLC Nedir?"):
    st.markdown("""
    **OLC 3 Seviyeli Haber Okuma Sistemi:**

    - 📰 **OPEN** - Hızlı Bakış: 2 cümlelik özet (5 saniye)
    - 📚 **LEARN** - Detaylı: Bullet point'lerle detay (30 saniye)
    - 📄 **CLOSE** - Tam Metin: Haberin tamamı + kaynak (2 dakika)

    **Nasıl Kullanılır?**
    1. OPEN ile hızlıca tarayın
    2. İlginizi çeken haberlerde LEARN'e tıklayın
    3. Konuyu bitirmek için CLOSE'a gidin
    """)

st.divider()

# Sidebar - Filtreler
with st.sidebar:
    st.header("🔍 Filtreler")

    kategoriler = ["Tümü", "spor", "teknoloji", "borsa", "kitap"]
    secili_kategori = st.selectbox("📂 Kategori", kategoriler)

    sentiments = ["Tümü", "olumlu", "nötr", "olumsuz"]
    secili_sentiment = st.selectbox("😊 Duygu Durumu", sentiments)

    ai_islendi = st.checkbox("🤖 Sadece AI İşlenmiş", value=True)

    st.divider()

    st.header("📊 İstatistikler")
    try:
        stats_response = requests.get(f"{BACKEND_URL}/stats/sentiment", timeout=10)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            st.metric("📰 Toplam Haber", stats['total'])

            breakdown = stats.get('breakdown', {})
            for sentiment, data in breakdown.items():
                emoji = SENTIMENT_EMOJI.get(sentiment, "😐")
                st.metric(
                    f"{emoji} {sentiment.capitalize()}",
                    data['count'],
                    f"{data['percentage']:.1f}%"
                )
    except:
        pass

# Ana içerik
st.subheader("🔍 Arama")

col_search, col_button = st.columns([4, 1])

with col_search:
    search_query = st.text_input(
        "Başlık veya içerikte ara:",
        placeholder="Örn: Yapay zeka, Roket, Bitcoin, ...",
        label_visibility="collapsed"
    )

with col_button:
    search_button = st.button("🔍 Ara", use_container_width=True)

st.divider()

st.subheader("📰 Haberler")


# Haberleri getir
try:
    params = {}
    if secili_kategori != "Tümü":
        params['kategori'] = secili_kategori

    response = requests.get(f"{BACKEND_URL}/haberler", params=params, timeout=30)

    if response.status_code == 200:
        data = response.json()
        haberler = data['haberler']

        # Filtreler (client-side)
        if secili_sentiment != "Tümü":
             haberler = [h for h in haberler if h.get('sentiment_label') == secili_sentiment]

        # AI İşlenmiş filtresi - flash_ozet kontrolü
        if ai_islendi:
             haberler = [h for h in haberler
                        if h.get('flash_ozet')
                        and h.get('flash_ozet', '').strip()
                        and len(h.get('flash_ozet', '')) > 20]

        if search_query:
            search_lower = search_query.lower()
            haberler = [h for h in haberler
                        if search_lower in h.get('baslik', '').lower()
                        or search_lower in h.get('flash_ozet', '').lower()
                        or search_lower in h.get('detayli_ozet', '').lower()]

        # Sonuçlar
        st.success(f"✅ {len(haberler)} haber bulundu")

        # Haberleri göster
        if len(haberler) == 0:
            st.warning("Bu filtrelere uygun haber bulunamadı.")
        else:
            for haber in haberler[:20]:
                show_haber_card(haber)

            if len(haberler) > 20:
                st.info(f"💡 {len(haberler) - 20} haber daha var. Filtreleri kullanarak daraltın.")

    else:
        st.error(f"❌ Backend hata: {response.status_code}")

except Exception as e:
    st.error(f"❌ Bağlantı hatası: {str(e)}")
    st.info("💡 Backend uyuyor olabilir. 30 saniye bekleyip tekrar deneyin.")
