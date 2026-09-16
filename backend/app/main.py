from fastapi import FastAPI     #  FastApı uygulaması ile API yapımı görmek için(WEB framework)
from fastapi.middleware.cors import CORSMiddleware      #   Frontend'in ulaşması için güvenli bir şekilde(İzin olup olmadığını kontrol eder istek daha gelmeden yoldayken).

from .core.config import settings       #Uygulama bilgileri
from .api import haberler, ai       #  haber.py ile ai.py kodlarımızı alıyor

# FastAPI app oluştur
app = FastAPI(      #  Web framework nesnesi
    title=settings.PROJECT_NAME,
    description="OLC - Open Learn Close | AI-powered haber özet platformu",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (Kurallar ,kısıtlamalar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        #  Her yerden gelen isteklere açıktır.
    allow_credentials=True,     #  Kimlik verilerinin gönderilmesine izin var.
    allow_methods=["*"],        #  Bütün methodlara açık
    allow_headers=["*"],
)

# Health check endpoint API bağlantıları çalışıyor mu?
@app.get("/")
def root():
    """API root - health check"""
    return {
        "message": "OLC API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

# API routers ile API'ları ana projeye app'e bağlıyorum
app.include_router(haberler.router, prefix="/api/v1", tags=["haberler"])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"])
#  Bu iki satır çok kritik başka dosyalarda tanımlı olan endpointleri alıp bağlanmakta app uygulamasının içine kaydetmekte.
#  Bu kod ile teker teker route yazma işleminden kurtulmuş oluyoruz.
#  Başka dosyalarda tanımlanmış endpoint’leri alır, prefix ile URL yapısını oluşturur ve FastAPI’nin merkezi route tablosuna kaydederek API’nin gerçekten çalışmasını sağlar.