"""
AI Service - Anthropic Claude API Integration
OLC (Open Learn Close) 3 seviyeli özet sistemi için
"""
import anthropic
from typing import Dict, List, Optional
import json
import re

from .ai_service_mock import mock_ai_service
USE_REAL_AI = False 

from ..core.config import settings


class AIService:
    """Anthropic Claude API ile haber analizi"""
    
    def __init__(self):
        """Initialize Anthropic client"""
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY bulunamadı! .env dosyasını kontrol edin.")
        
        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
        self.model = "claude-sonnet-4-20250514"
    
    def generate_flash_ozet(self, tam_metin: str) -> str:
        """
        OPEN seviyesi: 2 cümle özet
        Liste görünümünde gösterilecek
        """
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
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=150,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            ozet = message.content[0].text.strip()
            
            # Temizlik: Başlık varsa kaldır
            ozet = re.sub(r'^#+\s.*?\n', '', ozet)
            ozet = re.sub(r'^Özet:\s*', '', ozet, flags=re.IGNORECASE)
            
            return ozet
            
        except Exception as e:
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
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=400,
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
    
    def analyze_sentiment(self, tam_metin: str) -> Dict[str, any]:
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
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            result = json.loads(response_text)
            
            # Validation
            skor = float(result.get("skor", 0.0))
            skor = max(-1.0, min(1.0, skor))  # Clamp to [-1, 1]
            
            label = result.get("label", "nötr")
            if label not in ["olumlu", "nötr", "olumsuz"]:
                label = "nötr"
            
            return {"skor": skor, "label": label}
            
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
            
            # JSON parse
            response_text = re.sub(r'^```json\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
            
            keywords = json.loads(response_text)
            
            # Validation: liste mi, string elemanları var mı
            if not isinstance(keywords, list):
                keywords = []
            
            keywords = [str(k).lower().strip() for k in keywords if k]
            keywords = keywords[:8]  # Max 8
            
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
ai_service = AIService()

if USE_REAL_AI:
    ai_service = AIService()
else:
    ai_service = mock_ai_service
