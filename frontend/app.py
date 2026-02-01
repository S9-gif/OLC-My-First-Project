import streamlit as st
import requests     #  HTTP istekleri için bu modüldeki bazı fonksiyonları kullanacağım.
import pandas as pd     #  İstatistiksel analizler için okuldan da bildiğim pandas. 
from datetime import datetime





# Sayfa konfigürasyonu
st.set_page_config(
    page_title="OLC - Open Learn Close",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
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
""", unsafe_allow_html=True)        #  Normalde markdown içine yaılanlar metin olarak algılanır fakat bu True ile içine yazılan HHTML CSS kodlarının kod olarak kullanılmasını sağlıyorum.

# Backend URL
BACKEND_URL = "https://olc-backend.onrender.com/api/v1"     #  Backend'e ulaşıyorum API ile ilerleyen yerkerde backend'in bütün kısımlarını /haber vs... ile çağıracağız. ana kök API.

# Sentiment emoji mapping ile backend'deki sentiment analizlerine emoji ile ekleme yapıyorum.
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
def show_haber_card(haber):     #   Her bir haber için oluşturulacak haber kartı bunu da haber objeleri ile yapacak.Haber objelerinden yararlanacak.
    sentiment = haber.get('sentiment_label', 'nötr')        #  Haber objesinden sentiment_label bilgisini çeker ve default değer olarak nötr almasını istiyorum değer yoksa
    kategori = haber.get('kategori', 'genel')       #  Aynısı kategoriyi çekerken de yapıyoruz.Kategori varsa alınır yoksa default değer olarak gözükür.
    
    # Kart container
    with st.container():        #  Her haber nesnesi için sınırlar.
        # Başlık
        st.markdown(f"### 📰 {haber['baslik']}")        #  Alınan haber onjesinin başık bilgisini başlık olarak kullanıyorum.
        
        # Metadata
        emoji_sentiment = SENTIMENT_EMOJI.get(sentiment, "😐")      #  Default değerleri ile birlikte sentiment değerini ve kategorisini ackend'den get ediyorum.
        emoji_kategori = KATEGORI_EMOJI.get(kategori, "📰")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"{emoji_sentiment} **{sentiment.upper()}**")       #  ** 'lar metin türü için
        with col2:
            st.markdown(f"{emoji_kategori} **{kategori.upper()}**")
        with col3:
            st.markdown(f"🆔 ID: {haber['id']}")
        
        # 📰 OPEN - Flash Özet (Her zaman görünür)
        st.markdown("#### 📰 OPEN - Hızlı Bakış")
        flash_ozet = haber.get('flash_ozet', 'Özet henüz oluşturulmadı')
        st.info(flash_ozet)
        
        # 📚 LEARN - Detaylı Özet (Expander)
        with st.expander("📚 LEARN - Detaylı Özet"):        #  Tıklanınca isteğe bağlı açılacak expender sayesinde.
            detayli_ozet = haber.get('detayli_ozet', 'Detaylı özet henüz oluşturulmadı')        #  haber nesnesindeki detaylı özeti alır.
            if detayli_ozet:
                # Bullet point'leri parse et
                lines = detayli_ozet.split('\n')        #  Eğer detaylı özet varsa bulunan \n ler ile ayırırırım maddeleri burda parse ederim.(Bunu lines değişkenine atadım sonra linesda parse ettim.)
                for line in lines:
                    if line.strip():
                        st.markdown(line)
            else:
                st.warning("Detaylı özet henüz hazır değil")
        
        # 📄 CLOSE - Tam Metin (Expander)
        with st.expander("📄 CLOSE - Tam Metin & Kaynak"):
            tam_metin = haber.get('tam_metin', 'Tam metin bulunamadı')
            st.markdown(tam_metin)
            
            st.divider()        
            
            # Kaynak link
            kaynak_url = haber.get('kaynak_url', '#')
            kaynak_adi = haber.get('kaynak_adi', 'Kaynak')
            st.markdown(f"**📰 Kaynak:** [{kaynak_adi}]({kaynak_url})")
            
            # Anahtar kelimeler
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
with st.sidebar:        #  Bu alandaki bütün işlemler sidebar alanında
    st.header("🔍 Filtreler")
    
    # Kategori filtresi
    kategoriler = ["Tümü", "spor", "teknoloji", "borsa", "kitap"]
    secili_kategori = st.selectbox("📂 Kategori", kategoriler)
    
    # Sentiment filtresi
    sentiments = ["Tümü", "olumlu", "nötr", "olumsuz"]
    secili_sentiment = st.selectbox("😊 Duygu Durumu", sentiments)
    
    # AI işlenmiş filtresi
    ai_islendi = st.checkbox("🤖 Sadece AI İşlenmiş", value=True)
    
    st.divider()
    
    # Canlı istatistik almak için
    st.header("📊 İstatistikler")
    try:        #  İlgili bilgileri almaya çalışırken hata oluşursa uygulama çökmesin.
        stats_response = requests.get(f"{BACKEND_URL}/stats/sentiment", timeout=10)     #  Başarısız olursa donmaması için 10 saniye bekleme süresi.
        if stats_response.status_code == 200:           #  Başarılı bir şekilde alırsak status code 200 olsun
            stats = stats_response.json()       #  JSON veri tipini python objesine çevirdim.
            st.metric("📰 Toplam Haber", stats['total'])        #  Çıktı veriyorum.
            
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
    # API parametreleri
    params = {}     #  Boş bir dictionary yapı kategori ve bu kategorinin değerini tutacak.
    if secili_kategori != "Tümü":       #  Seöili kategori tümü değilse
        params['kategori'] = secili_kategori        #  Mevcut parametre kategori değeridir.
    
    response = requests.get(f"{BACKEND_URL}/haberler", params=params, timeout=30)       #  Backend'den çekilecek url bu parametre ile belirlenecek ve url'nin sonuna eklenir.
    
    if response.status_code == 200:     #  API başarılı bir şekilde alınırsa bunu True olarak alıcam.
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
             
        if search_query:        #  Serach alanı dolu yani True ise
            search_lower = search_query.lower()     #  Yazılanların hepsini küçük harf olarak aldım.
            haberler = [h for h in haberler         #  Şartların sağlandığı haberleri haberler listeme ekleyecek olan küçük algoritamız.
                        if search_lower in h.get('baslik', '').lower()      #  Serach querry 'deki değer gezilen haberin başlığı ile uyuşuyorsa.
                        or search_lower in h.get('flash_ozet', '').lower()      #  ya da flash özetten bir kelime ile uyuşuyorsa
                        or search_lower in h.get('detayli_ozet', '').lower()]       #Yada detaylı özetten bir kelime ile uyuşuyorsa bunu haberler listeme eklerim (Haberi).
        
        # Sonuçlar
        st.success(f"✅ {len(haberler)} haber bulundu")
        
        # Haberleri göster
        if len(haberler) == 0:      #  Haberler listem boşsa haber bulamamıştır.
            st.warning("Bu filtrelere uygun haber bulunamadı.")
        else:
            for haber in haberler[:20]:  # İlk 20 haber
                show_haber_card(haber)
            
            if len(haberler) > 20:
                st.info(f"💡 {len(haberler) - 20} haber daha var. Filtreleri kullanarak daraltın.")
            
    else:
        st.error(f"❌ Backend hata: {response.status_code}")
        
except Exception as e:
    st.error(f"❌ Bağlantı hatası: {str(e)}")
    st.info("💡 Backend uyuyor olabilir. 30 saniye bekleyip tekrar deneyin.")