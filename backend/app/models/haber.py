from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from ..core.database import Base


class Haber(Base):
    __tablename__ = "haberler"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Temel bilgiler
    baslik = Column(String(500), nullable=False)
    kategori = Column(String(50), nullable=False, index=True)
    
    # 3 seviyeli OLC özet sistemi
    flash_ozet = Column(Text)
    detayli_ozet = Column(Text)
    tam_metin = Column(Text)
    
    # Kaynak
    kaynak_url = Column(String(1000))
    kaynak_adi = Column(String(200))
    yazar = Column(String(200))
    
    # Tarihler
    yayin_tarihi = Column(DateTime(timezone=True))
    olusturma_tarihi = Column(DateTime(timezone=True), server_default=func.now())
    guncelleme_tarihi = Column(DateTime(timezone=True), onupdate=func.now())
    
    # AI sonuçları
    sentiment_skor = Column(Float)
    sentiment_label = Column(String(20))
    anahtar_kelimeler = Column(JSON)
    
    # Metrikler
    okunma_sayisi = Column(Integer, default=0)
    tam_metin_acilma = Column(Integer, default=0)
    
    # Flags
    ai_islendi = Column(Integer, default=0)
    yayinda = Column(Integer, default=1)
    
    def __repr__(self):
        return f"<Haber {self.id}: {self.baslik[:30]}...>"
