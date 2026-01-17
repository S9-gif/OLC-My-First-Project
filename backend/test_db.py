from app.core.database import SessionLocal
from app.models.haber import Haber
from datetime import datetime

def test_database():
    print("🧪 Database bağlantısı test ediliyor...\n")
    
    db = SessionLocal()
    
    try:
        # Test haberi oluştur
        test_haber = Haber(
            baslik="🎉 İlk Haber - OLC Platform Test",
            kategori="test",
            flash_ozet="Bu OLC platformunun ilk test haberidir.",
            kaynak_adi="OLC Test",
            yayin_tarihi=datetime.now()
        )
        
        # Database'e ekle
        db.add(test_haber)
        db.commit()
        db.refresh(test_haber)
        
        print(f"✅ Haber eklendi!")
        print(f"   ID: {test_haber.id}")
        print(f"   Başlık: {test_haber.baslik}")
        print(f"   Kategori: {test_haber.kategori}\n")
        
        # Geri oku
        haber = db.query(Haber).filter(Haber.id == test_haber.id).first()
        print(f"✅ Haber okundu!")
        print(f"   Başlık: {haber.baslik}\n")
        
        # Tüm haberleri say
        count = db.query(Haber).count()
        print(f"✅ Toplam haber sayısı: {count}\n")
        
        # Test haberini sil
        db.delete(test_haber)
        db.commit()
        print(f"✅ Test haberi silindi\n")
        
        print("🎉 Database bağlantısı tamamen çalışıyor!")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
