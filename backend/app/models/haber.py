from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from ..core.database import Base        #.. Nokta ile üst klasöre çıkıyorum.Göreceli import
        ## Ve Base sayesinde DB ile python eşlenmesi sağlanır bu ORM için çok kritiktir.


class Haber(Base):      #Base'i bizim için parent bir sınıftır ve DB eşlemesini yapacaktır onun altında pythondaki class'ımı DB için oluşturabilirim.
    __tablename__ = "haberler"#Table ismim
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)      #index True ile her gelen yeni veriye sayı ataya,primary key olacak ve int veri tipinde olacak olan id kolonum.
    
    # Temel bilgiler
    baslik = Column(String(500), nullable=False)        #Başlık kolonum sting veri tipinde ve nullabe yani boş olabilir için false yani olamaz olarak belirttik.
    kategori = Column(String(50), nullable=False, index=True)
    
    # 3 seviyeli OLC özet sistemi
    flash_ozet = Column(Text)       # flash_ozet isimli kolonum
    detayli_ozet = Column(Text)
    tam_metin = Column(Text)
    
    # Kaynak
    kaynak_url = Column(String(1000))       #  Aynı şekilde diğer lazım olacak bilgilerim için de DB'de bölümler oluşturuyorum ve bunu text olarak oluşturuyorum
    kaynak_adi = Column(String(200))
    yazar = Column(String(200))
    
    # Tarihler
    yayin_tarihi = Column(DateTime(timezone=True))
    olusturma_tarihi = Column(DateTime(timezone=True), server_default=func.now())       #  Oluşturma tarihini DB'in belirlemesini istediğim için sqlalchemy.sql deki func fonksiyonunu zaten import etmiştim.
    guncelleme_tarihi = Column(DateTime(timezone=True), onupdate=func.now())
    
    # AI sonuçları
    sentiment_skor = Column(Float)
    sentiment_label = Column(String(20))
    anahtar_kelimeler = Column(JSON)
    
    # Metrikler
    okunma_sayisi = Column(Integer, default=0)      #  İşlenmese bile default değeri işlenmediğini belirtsin bu nedenle 0
    tam_metin_acilma = Column(Integer, default=0)
    
    # Flags
    ai_islendi = Column(Integer, default=0)
    yayinda = Column(Integer, default=1)
    
    def __repr__(self):     #repr fonksiyonu geliştirici yani ben için debuglama da hatayı doğru anlamaı sağlayacak bir fonksiyon nesneleri bir stinge çevirmesi gerektiğinde  bu fonksiyon çalışır.
        return f"<Haber {self.id}: {self.baslik[:30]}...>"
