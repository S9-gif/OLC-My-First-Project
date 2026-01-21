"""
Mock AI Service - Development için basit AI simülasyonu
Gerçek AI (Anthropic/OpenAI) yerine geçer
İleride gerçek AI ile değiştirilebilir
"""
from typing import Dict, List
import random
import re


class MockAIService:
    """Basit AI simülasyonu - Ücretsiz"""
    
    def __init__(self):
        """Mock service - API key gerekmez"""
        print("⚠️  Mock AI Service başlatıldı (Gerçek AI değil)")
    
    def generate_flash_ozet(self, tam_metin: str) -> str:
        """
        Basit özet: İlk 2 cümle
        """
        # Cümlelere ayır
        sentences = re.split(r'[.!?]+', tam_metin)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # İlk 2 cümle
        if len(sentences) >= 2:
            return f"{sentences[0]}. {sentences[1]}."
        elif len(sentences) == 1:
            return f"{sentences[0]}."
        else:
            return "Özet oluşturulamadı."
    
    def generate_detayli_ozet(self, tam_metin: str) -> str:
        """
        Basit özet: İlk 4-5 cümle madde halinde
        """
        sentences = re.split(r'[.!?]+', tam_metin)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # İlk 5 cümle
        selected = sentences[:5]
        
        # Madde halinde
        ozet = ""
        for i, sentence in enumerate(selected, 1):
            ozet += f"• {sentence}\n"
        
        return ozet.strip() if ozet else "• Detaylı özet oluşturulamadı."
    
    def analyze_sentiment(self, tam_metin: str) -> Dict[str, any]:
        """
        Basit sentiment: Pozitif/negatif kelime sayısı
        """
        metin_lower = tam_metin.lower()
        
        # Basit pozitif/negatif kelimeler
        pozitif_kelimeler = [
            'başarı', 'iyi', 'harika', 'mükemmel', 'yükseliş', 'artış', 
            'kazanç', 'olumlu', 'gelişme', 'rekor', 'zafer', 'kazandı'
        ]
        
        negatif_kelimeler = [
            'kötü', 'başarısız', 'düşüş', 'azalış', 'kayıp', 'olumsuz',
            'kriz', 'sorun', 'tehlike', 'çöküş', 'kaybetti', 'felaket'
        ]
        
        pozitif_say = sum(1 for kelime in pozitif_kelimeler if kelime in metin_lower)
        negatif_say = sum(1 for kelime in negatif_kelimeler if kelime in metin_lower)
        
        # Skor hesapla
        if pozitif_say + negatif_say == 0:
            skor = 0.0
            label = "nötr"
        else:
            skor = (pozitif_say - negatif_say) / (pozitif_say + negatif_say)
            
            if skor > 0.3:
                label = "olumlu"
            elif skor < -0.3:
                label = "olumsuz"
            else:
                label = "nötr"
        
        return {"skor": round(skor, 2), "label": label}
    
    def extract_keywords(self, tam_metin: str, baslik: str = "") -> List[str]:
        """
        Basit keyword extraction: En sık geçen kelimeler
        """
        # Metni temizle
        metin = (baslik + " " + tam_metin).lower()
        
        # Stop words (Türkçe yaygın kelimeler)
        stop_words = {
            've', 'bir', 'bu', 'için', 'ile', 'da', 'de', 'ise', 'ki',
            'mi', 'mı', 'mu', 'mü', 'ama', 'fakat', 'ancak', 'çok',
            'daha', 'en', 'her', 'gibi', 'göre', 'kadar', 'sonra',
            'olan', 'olarak', 'üzere', 'var', 'yok', 'olan', 'oldu'
        }
        
        # Kelimelere ayır
        words = re.findall(r'\b[a-züğışöç]{3,}\b', metin)
        
        # Stop words filtrele
        words = [w for w in words if w not in stop_words]
        
        # Frekans say
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # En sık 8 kelime
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, freq in sorted_words[:8]]
        
        return keywords
    
    def process_haber(self, tam_metin: str, baslik: str = "") -> Dict:
        """
        Tam haber analizi - Mock versiyonu
        """
        print(f"🤖 Mock AI işleme başladı... (Haber uzunluğu: {len(tam_metin)} karakter)")
        
        flash = self.generate_flash_ozet(tam_metin)
        print("  ✅ Flash özet oluşturuldu (basit)")
        
        detayli = self.generate_detayli_ozet(tam_metin)
        print("  ✅ Detaylı özet oluşturuldu (basit)")
        
        sentiment = self.analyze_sentiment(tam_metin)
        print(f"  ✅ Sentiment analizi: {sentiment['label']} ({sentiment['skor']:.2f})")
        
        keywords = self.extract_keywords(tam_metin, baslik)
        print(f"  ✅ Anahtar kelimeler: {', '.join(keywords[:5])}")
        
        print("🎉 Mock AI işleme tamamlandı!")
        
        return {
            "flash_ozet": flash,
            "detayli_ozet": detayli,
            "sentiment_skor": sentiment["skor"],
            "sentiment_label": sentiment["label"],
            "anahtar_kelimeler": keywords
        }


# Singleton instance
mock_ai_service = MockAIService()
