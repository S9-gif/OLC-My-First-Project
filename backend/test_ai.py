"""AI Service test - Kısa test"""
from app.services.ai_service import ai_service

# Test haberi (kısa)
test_haber = """
Bitcoin, tarihinde ilk kez 100,000 dolar seviyesini aştı. Kripto para piyasasındaki 
bu tarihi zirve, yatırımcılar arasında büyük heyecan yarattı. Uzmanlar, kurumsal 
yatırımcıların artan ilgisinin bu yükselişte önemli rol oynadığını belirtiyor. 
Ancak, yüksek volatilite nedeniyle dikkatli olunması gerektiği vurgulanıyor.
"""

print("🧪 AI Service Test Başlıyor...\n")

try:
    # 1. Flash özet
    print("1️⃣ Flash Özet Test:")
    flash = ai_service.generate_flash_ozet(test_haber)
    print(f"   {flash}\n")
    
    # 2. Detaylı özet
    print("2️⃣ Detaylı Özet Test:")
    detayli = ai_service.generate_detayli_ozet(test_haber)
    print(f"   {detayli}\n")
    
    # 3. Sentiment
    print("3️⃣ Sentiment Analizi:")
    sentiment = ai_service.analyze_sentiment(test_haber)
    print(f"   Skor: {sentiment['skor']}")
    print(f"   Label: {sentiment['label']}\n")
    
    # 4. Keywords
    print("4️⃣ Anahtar Kelimeler:")
    keywords = ai_service.extract_keywords(test_haber, "Bitcoin 100K'yı geçti")
    print(f"   {', '.join(keywords)}\n")
    
    # 5. Tam işleme
    print("5️⃣ Tam İşleme (process_haber):")
    result = ai_service.process_haber(test_haber, "Bitcoin 100K")
    print(f"   ✅ Tüm alanlar oluşturuldu!\n")
    
    print("🎉 Tüm testler başarılı!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
