from pydantic import BaseModel      #  API 'lar için ana sınıf(pydantic de ver idoğrulama gibi işlemleri yapan kütüphanem)
from typing import Optional, List       #  Veri tipi kontrolü
from datetime import datetime       


class HaberBase(BaseModel):     #  Bu class sayesinde haber objeleri oluşturulacbilinecek
    """Temel haber alanları"""
    baslik: str
    kategori: str
    kaynak_adi: Optional[str] = None        #  İşte burda opsiyonel olarak typing import Optional, List sayesinde veri tipini beliirleyebiliyorum.Bu da bana esneklik kazandırıyor.
    kaynak_url: Optional[str] = None


class HaberCreate(HaberBase):       #  Üstte yer alan HaberBase class'ının özelliklerinden yararlanan ara bir obje tam haberi ilgili özellikleri ile tutacak.
    """Haber oluştururken gönderilecek (N8N kullanacak)"""
    tam_metin: Optional[str] = None
    yayin_tarihi: Optional[datetime] = None


class HaberUpdate(BaseModel):       #  Asıl önenmli olan ve istediğimiz objemiz bunları nasıl yapacağını AI modele prompt ile belirteceğiz ona bilgileri verebileceği bir kutu ,alan oluşturuyorum.
    """AI tarafından güncellenecek alanlar"""
    flash_ozet: Optional[str] = None
    detayli_ozet: Optional[str] = None
    sentiment_skor: Optional[float] = None
    sentiment_label: Optional[str] = None
    anahtar_kelimeler: Optional[List[str]] = None
    ai_islendi: Optional[int] = None


class HaberResponse(HaberBase):     #  Backend-> Frontend için köprü  ve turmasını istediğim bilgiler(ekstra olarak HaberBase'den de miras alır.)
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
    
    class Config:       #  Burda ORM ile oluşturulan (models/haber.py) nesne şeklindeki bilgileri de alıp API için kontrol edenilmesini sağlıyorum.
        from_attributes = True


class HaberListResponse(BaseModel):       #  Genel DB bilgilerimi de bir nesne olarak döndürücem.
    """Sayfalı liste response"""
    total: int
    page: int
    page_size: int
    haberler: List[HaberResponse]





        #   Bu sayede API'lar için ilgili doğrulama objelerini oluşturmuş olduk.
    
    