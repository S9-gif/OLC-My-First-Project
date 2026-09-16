from sqlalchemy import create_engine        #  Veri Tabanı bağlantısı kurmak için lazım olan paketimiz.Kodunu yazarken DB url'miz ile bağlantıyı kuracağız.
from sqlalchemy.ext.declarative import declarative_base     #  Oluşturulan ORM nesnelerimi Veri tabanına table olarak yerleştirir.
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)       #  DB bağlantısı url başka bir dosyada tanımlı olduğundan direkt olarak böyle yazabilirim.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     #  Asıl baplantı burdadır yapılan değişiklikler için commitleme isteyen ve bind=engine ile belirttiğim DB e bağlanan bir session.
Base = declarative_base()       #  ORM ile üretilen haber nesnelerini

def get_db():
    db = SessionLocal()
    try:
        yield db        #  Sürekli olarak yenileneceği için return etmedim geçici olarak turmasını istiyoruz.yield yerine return olsaydı DB açık kalırdı
                        #  !yield ile denenen açılma başarılı olur ve bilgi alınırsa try'dan sonra gelen finally ile açılan bağlantı kapatılır.!
    finally:
        db.close()


#  db değişkeni üzerinde istenilen bağlantı oluşturulur ve finally ile açılan sekme kapatılır ????
#  Temel olarak session çağrıları atan ve bunları kapatan bir kod bu ama biraz kafam karıştı ???