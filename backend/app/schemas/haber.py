from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HaberBase(BaseModel):
    """Temel haber alanları"""
    baslik: str
    kategori: str
    kaynak_adi: Optional[str] = None
    kaynak_url: Optional[str] = None


class HaberCreate(HaberBase):
    """Haber oluştururken gönderilecek (N8N kullanacak)"""
    tam_metin: Optional[str] = None
    yayin_tarihi: Optional[datetime] = None


class HaberUpdate(BaseModel):
    """AI tarafından güncellenecek alanlar"""
    flash_ozet: Optional[str] = None
    detayli_ozet: Optional[str] = None
    sentiment_skor: Optional[float] = None
    sentiment_label: Optional[str] = None
    anahtar_kelimeler: Optional[List[str]] = None
    ai_islendi: Optional[int] = None


class HaberResponse(HaberBase):
    """API'den dönen haber (Frontend kullanacak)"""
    id: int
    flash_ozet: Optional[str] = None
    detayli_ozet: Optional[str] = None
    sentiment_skor: Optional[float] = None
    sentiment_label: Optional[str] = None
    anahtar_kelimeler: Optional[List[str]] = None
    yayin_tarihi: Optional[datetime] = None
    olusturma_tarihi: datetime
    okunma_sayisi: int
    
    class Config:
        from_attributes = True


class HaberListResponse(BaseModel):
    """Sayfalı liste response"""
    total: int
    page: int
    page_size: int
    haberler: List[HaberResponse]
