#  endpoint ile claude arasında yöneten bir katman


"""
AI Service - Anthropic Claude API Integration
OLC (Open Learn Close) 3 seviyeli özet sistemi için
"""
import anthropic        #  Model ile iletişim kurabilmemi sağlayacak olan modül
from typing import Dict, List, Optional     #  AI servislerinin döndürdüğü veri belirtsizliğini stabil etmede kullnacağım.
import json     #  AI' dan gelen response'leri json veri tipine çevirmek için gerekli olan modülüm.
import re       #  Gereksiz ifadeleri temizlemek için kulanacağım re modülü

from .ai_service_mock import mock_ai_service
USE_REAL_AI = False         #  Projei para harcamadan yapmak istediğim için biraz ödün vermem gerekiyor bu da Mock aı modelini kullanmam gerektiği anlamına geliyor.
                            #  Ama kodun sonuna bunu istediğim zaman düzeltmemi sağlayan bir if koşulu koydum.
from ..core.config import settings      #  API key gibi gizli tutulması gereken bilgilerimi settings nesnemden çekeceğim

class AIService:        #  AI ile ilgili bütün işlemleri tek bir nesnede tutucam(AI Service).
    """Anthropic Claude API ile haber analizi"""        
    
    def __init__(self):     
        """Initialize Anthropic client"""
        if not settings.ANTHROPIC_API_KEY:      #  İlk başta endpoint'e bağlanamadıysa direkt olarak hata çıktısı veriyor.
            raise ValueError("ANTHROPIC_API_KEY bulunamadı! .env dosyasını kontrol edin.")      #  Debug için önemli
        
        self.client = anthropic.Anthropic(      #  Claude AI 'a giriş (client)
            api_key=settings.ANTHROPIC_API_KEY
        )
        self.model = "claude-sonnet-4-20250514"     #  Kullanılacak claude modeli
    
    def generate_flash_ozet(self, tam_metin: str) -> str:       #  Daha önce oluşturduğumuz haber nesnesinde str veri tipinde haberi aldık  bir argüman gibi ve bunu AI modeline verdik.
        """
        OPEN seviyesi: 2 cümle özet
        Liste görünümünde gösterilecek
        """
                #  Promt ile verilen bu argüman ile ne yapmasını istediğimizi prompt engineering adı altında verdik
        prompt = f"""       
        Aşağıdaki Türkçe haber metnini TAM OLARAK 2 cümle ile özetle.
        
        Kurallar:
        - Sadece 2 cümle yaz (nokta ile bitir)
        - Objektif ve net ol
        - En önemli bilgileri ver
        - Başlık yazma, direkt özete gir
        
        Haber:
        {tam_metin[:2000]}          
        
        2 cümle özet:
        """
        #  Tam metini token'i de geçmemesi için kısıtladım AI modeli burasını kullanacak.(  {tam_metin[:2000]} )
        try:        #  Debug işini kolaylaştırsın diye try içinde 
            message = self.client.messages.create(
                model=self.model,       #  Tanımlanan modelde
                max_tokens=150,         #  Kullanavileceği mac token sayısı
                temperature=0.3,        #  Düşük yaratıcılık hata ve saçmalamayı engellemek için
                messages=[{"role": "user", "content": prompt}]      #  AI modelinin daha detaylı olması için rolleri ve neyin ne olduğunu da belirtiyorum.
            )
            
            ozet = message.content[0].text.strip()      #  Mesajı özet adı altında alıyorum ve sağlı sollu temizliyorum
            
            # Temizlik: Başlık varsa kaldır
            ozet = re.sub(r'^#+\s.*?\n', '', ozet)      #  Alınan mesajı temizler
            ozet = re.sub(r'^Özet:\s*', '', ozet, flags=re.IGNORECASE)
        
            
            return ozet     #  Temizlenen haberi al
            
        except Exception as e:      #Debug için except satırı.
            print(f"Flash özet hatası: {e}")
            return "Özet oluşturulamadı."
    
    def generate_detayli_ozet(self, tam_metin: str) -> str:
        """
        LEARN seviyesi: 4-5 madde detaylı özet
        Modal/detay sayfasında gösterilecek
        """
        prompt = f"""
        Aşağıdaki Türkçe haber metnini 4-5 madde ile detaylı özetle.
        
        Format:
        • Madde 1 (en önemli bilgi)
        • Madde 2
        • Madde 3
        • Madde 4
        • Madde 5 (varsa)
        
        Kurallar:
        - Her madde 1-2 cümle
        - Bullet point (•) kullan
        - Objektif dil
        - Kronolojik sıra (varsa)
        - Başlık yazma
        
        Haber:
        {tam_metin[:3000]}
        
        Detaylı özet:
        """
        #  Detaylı özet için daha fazla bilgiye ihtiyacı olabilir.
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=400,     #Detaylı özet yarattığım için token sayısını arttırdım
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ozet = message.content[0].text.strip()
            
            # Temizlik
            ozet = re.sub(r'^#+\s.*?\n', '', ozet)
            ozet = re.sub(r'^Detaylı Özet:\s*', '', ozet, flags=re.IGNORECASE)
            
            return ozet
            
        except Exception as e:
            print(f"Detaylı özet hatası: {e}")
            return "• Detaylı özet oluşturulamadı."
    
    def analyze_sentiment(self, tam_metin: str) -> Dict[str, any]:      #  Geri alınacak olan verinin dict şeklinde verilmesini istiyorum.
        """
        Sentiment analizi: skor ve label
        
        Returns:
            {"skor": 0.75, "label": "olumlu"}
        """
        prompt = f"""
        Bu Türkçe haberin sentiment'ini (duygu tonunu) analiz et.
        
        Sadece şu JSON formatında cevap ver (başka bir şey yazma):
        {{"skor": 0.75, "label": "olumlu"}}
        
        Skor kuralları:
        - -1.0 ile 1.0 arası float
        - -1.0: Çok olumsuz (felaket, kriz, ölüm)
        - -0.5: Olumsuz (kötü haber, sorun)
        - 0.0: Nötr (objektif, tarafsız)
        - 0.5: Olumlu (iyi haber, gelişme)
        - 1.0: Çok olumlu (zafer, başarı, sevinç)
        
        Label kuralları:
        - "olumsuz": skor < -0.3
        - "nötr": -0.3 <= skor <= 0.3
        - "olumlu": skor > 0.3
        
        Haber:
        {tam_metin[:2000]}
        
        JSON cevap:
        """
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # JSON parse
            # Bazen Claude ```json ... ``` ile sarabilir
            response_text = re.sub(r'^```json\s*', '', response_text)       #  response tect ile alınan json'u ayıklıyoruz.
            response_text = re.sub(r'\s*```$', '', response_text)
            
            result = json.loads(response_text)      #  Alınan json formatındaki veriyi python onjesine çevirir.
            
            # Validation AI'ın hata yapması durumunda sistemin sağlıklı bir şekilde çalışmasını devam ettirecek.
            skor = float(result.get("skor", 0.0))       # result'tan skor değerini alıyorum o nokta false çıkarsa ona nötr değer olan 0.0'ı atıyorum.
            skor = max(-1.0, min(1.0, skor))  # Clamp to [-1, 1] skor değeelirtilen default aralıkta yer almazsa onu aralığa geri çekerim yorumunu koruyarak.(Önce alttan sonra üsten sınırlamayı deniyorum ikisinden birinden mutlaka çıkıcaktr.)
            
            label = result.get("label", "nötr")     #  Label false ise nötr olarak değerlendirilir. 
            if label not in ["olumlu", "nötr", "olumsuz"]:      #  label deperli ama istenilen değerlerden değilse de label değerine nötr atanır .
                label = "nötr"
            
            return {"skor": skor, "label": label}       #  Sonra return ederim.
            
        except Exception as e:
            print(f"Sentiment analizi hatası: {e}")
            return {"skor": 0.0, "label": "nötr"}
    
    def extract_keywords(self, tam_metin: str, baslik: str = "") -> List[str]:
        """
        Anahtar kelimeler çıkar (5-8 kelime)
        
        Returns:
            ["bitcoin", "kripto", "yükseliş", ...]
        """
        prompt = f"""
        Bu Türkçe haberden 5-8 anahtar kelime çıkar.
        
        Kurallar:
        - Her kelime küçük harf
        - Türkçe karakterler kullan (ı, ğ, ş, vs.)
        - Tekil isimler (çoğul değil)
        - En önemli kavramlar
        - İsimler, yer adları, konseptler
        
        Sadece şu JSON formatında cevap ver:
        ["kelime1", "kelime2", "kelime3"]
        
        Başlık: {baslik}
        
        Haber:
        {tam_metin[:2000]}
        
        JSON array:
        """
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # JSON parse edilmesi
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            keywords = json.loads(response_text)        # jsondan python objesine çevirme
            
            # Validation: liste mi, string elemanları var mı
            if not isinstance(keywords, list):
                keywords = []
            
            keywords = [str(k).lower().strip() for k in keywords if k]
            keywords = keywords[:8]  # Max 8 keywod olsun ve hepsi küçük harfli olarak yazılsın
            
            return keywords
            
        except Exception as e:
            print(f"Keyword extraction hatası: {e}")
            return []
    
    def process_haber(self, tam_metin: str, baslik: str = "") -> Dict:
        """
        Tam haber analizi - Tüm AI işlemleri
        
        Returns:
            {
                "flash_ozet": "...",
                "detayli_ozet": "...",
                "sentiment_skor": 0.75,
                "sentiment_label": "olumlu",
                "anahtar_kelimeler": ["bitcoin", ...]
            }
        """
        print(f"🤖 AI işleme başladı... (Haber uzunluğu: {len(tam_metin)} karakter)")
        
        # Paralel olarak çağırabilirdik ama sıralı daha güvenli
        flash = self.generate_flash_ozet(tam_metin)
        print("  ✅ Flash özet oluşturuldu")
        
        detayli = self.generate_detayli_ozet(tam_metin)
        print("  ✅ Detaylı özet oluşturuldu")
        
        sentiment = self.analyze_sentiment(tam_metin)
        print(f"  ✅ Sentiment analizi: {sentiment['label']} ({sentiment['skor']:.2f})")
        
        keywords = self.extract_keywords(tam_metin, baslik)
        print(f"  ✅ Anahtar kelimeler: {', '.join(keywords)}")
        
        print("🎉 AI işleme tamamlandı!")
        
        return {
            "flash_ozet": flash,
            "detayli_ozet": detayli,
            "sentiment_skor": sentiment["skor"],
            "sentiment_label": sentiment["label"],
            "anahtar_kelimeler": keywords
        }


# Singleton instance
ai_service = AIService()        # Nesnemi oluşturdum

if USE_REAL_AI:
    ai_service = AIService()
else:
    ai_service = mock_ai_service


# Ve en sona yukarda bahsettiğim real AI ile mock AI için koşulum.Tek bir False değiştirmemde paralı gerçek AI modeline geçicem.