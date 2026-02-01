import streamlit as st
import json


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
    st.metric("📰 Toplam Haber", 127)
    st.metric("😊 Olumlu", 54, "42.5%")
    st.metric("😐 Nötr", 52, "40.9%")
    st.metric("😔 Olumsuz", 21, "16.5%")

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

# Mock veri
mock_haberler = [
    {
        "id": 10,
        "baslik": "Yapay Zeka Sağlık Sektöründü Dönüştürüyor",
        "kategori": "teknoloji",
        "sentiment_label": "olumlu",
        "kaynak_adi": "TechCrunch Türkiye",
        "kaynak_url": "https://techcrunch.tr/ai-saglik",
        "flash_ozet": "Yapay zeka teknolojileri, sağlık sektöründe devrim niteliğinde değişikliklere yol açıyor. Yeni geliştirilen AI algoritmaları, hastalıkların erken teşhisinde doktorlara yardımcı oluyor.",
        "detayli_ozet": "• Yapay zeka teknolojileri, sağlık sektöründe devrim niteliğinde değişikliklere yol açıyor\n• Yeni geliştirilen AI algoritmaları, hastalıkların erken teşhisinde doktorlara yardımcı oluyor\n• Özellikle kanser taramalarında yapay zeka, insan gözünün göremediği ayrıntıları tespit edebiliyor\n• Araştırmacılar, AI destekli tanı sistemlerinin hata oranını yüzde 30 oranında azalttığını belirtiyor",
        "tam_metin": "Yapay zeka sağlık endüstrisinde oyunun kurallarını değiştiriyor. Algoritmaların hastalıkları insanlardan daha erken tespit edebildiğini gösteren yeni araştırmalar ortaya çıktı.",
        "anahtar_kelimeler": ["yapay zeka", "sağlık", "AI", "tıp"]
    },
    {
        "id": 11,
        "baslik": "Bitcoin Son 24 Saatte Yüzde 15 Arttı",
        "kategori": "borsa",
        "sentiment_label": "olumlu",
        "kaynak_adi": "CryptoNews TR",
        "kaynak_url": "https://cryptonews.tr/bitcoin-rise",
        "flash_ozet": "Bitcoin'in değeri son 24 saat içinde önemli ölçüde yükseldi. Analistler, bu artışın kurumsal yatırımcıların geri dönmesiyle ilgili olduğunu söylüyor.",
        "detayli_ozet": "• Bitcoin'in değeri son 24 saat içinde %15 oranında yükseldi\n• Fiyat 45,000 doları aştı, yılın en yüksek seviyesine ulaştı\n• Kurumsal yatırımcılar yeniden piyasaya giriyor\n• Altcoinler de birlikte hareket ediyor",
        "tam_metin": "Kripto piyasalarında güçlü bir toparlanma yaşanıyor. Özellikle Bitcoin'in yıllık seviyeler yakalaması, pozitif sentiment gösteriyor.",
        "anahtar_kelimeler": ["Bitcoin", "kripto", "borsa", "yatırım"]
    },
    {
        "id": 12,
        "baslik": "Galatasaray Şampiyonluk Yarışında Öncü Konumda",
        "kategori": "spor",
        "sentiment_label": "nötr",
        "kaynak_adi": "Spor Haber",
        "kaynak_url": "https://spor.tr/galatasaray-sampiyonluk",
        "flash_ozet": "Galatasaray, ligin son haftasında önemli bir görüşüyü kazanarak şampiyonluk yarışında öncü konuma yükseldi.",
        "detayli_ozet": "• Galatasaray, karşılaştığı rakibine 3-2 ile galip geldi\n• Ekibin son 5 maçtaki performansı dikkat çekici seviyede\n• Teknik direktör oyunculardaki konsantrasyondan memnun\n• Sağlık sorunları olan iki oyuncu takıma kısa sürede dönebilir",
        "tam_metin": "Sarı-kırmızılar puan farkını 3'e çıkarttı. Takımın motivasyonu oldukça yüksek durumda.",
        "anahtar_kelimeler": ["Galatasaray", "futbol", "şampiyonluk", "spor"]
    }
]

st.success(f"✅ {len(mock_haberler)} haber bulundu")

for haber in mock_haberler:
    show_haber_card(haber)
