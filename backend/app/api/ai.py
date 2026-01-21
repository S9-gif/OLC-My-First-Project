"""
AI API Endpoints
Haber özet çıkarma ve sentiment analizi
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.haber import Haber
from ..schemas.haber import HaberResponse, HaberUpdate
from ..services.haber_service import HaberService
from ..services.ai_service import ai_service

router = APIRouter()


@router.post("/ai/process/{haber_id}", response_model=HaberResponse)
def process_haber_with_ai(
    haber_id: int,
    db: Session = Depends(get_db)
):
    """
    Haberi AI ile işle - OLC 3 seviyeli özet oluştur
    
    - **haber_id**: İşlenecek haberin ID'si
    
    İşlemler:
    1. Haberi getir (tam_metin olmalı)
    2. AI ile analiz et:
       - flash_ozet (OPEN - 2 cümle)
       - detayli_ozet (LEARN - 4-5 madde)
       - sentiment_skor ve sentiment_label
       - anahtar_kelimeler
    3. Haberi güncelle (ai_islendi = 1)
    4. Güncellenmiş haberi döndür
    """
    # 1. Haberi bul
    haber = db.query(Haber).filter(Haber.id == haber_id).first()
    
    if not haber:
        raise HTTPException(status_code=404, detail="Haber bulunamadı")
    
    # 2. tam_metin kontrolü
    if not haber.tam_metin or len(haber.tam_metin.strip()) < 50:
        raise HTTPException(
            status_code=400, 
            detail="Haber tam_metin içermiyor veya çok kısa (minimum 50 karakter)"
        )
    
    # 3. Zaten işlenmiş mi kontrol (opsiyonel - tekrar işlemeyi engellemek için)
    # if haber.ai_islendi == 1:
    #     raise HTTPException(status_code=400, detail="Haber zaten AI tarafından işlenmiş")
    
    # 4. AI ile işle
    try:
        ai_result = ai_service.process_haber(
            tam_metin=haber.tam_metin,
            baslik=haber.baslik
        )
        
        # 5. Haberi güncelle
        haber_update = HaberUpdate(
            flash_ozet=ai_result["flash_ozet"],
            detayli_ozet=ai_result["detayli_ozet"],
            sentiment_skor=ai_result["sentiment_skor"],
            sentiment_label=ai_result["sentiment_label"],
            anahtar_kelimeler=ai_result["anahtar_kelimeler"],
            ai_islendi=1
        )
        
        updated_haber = HaberService.update(db, haber_id, haber_update)
        
        if not updated_haber:
            raise HTTPException(status_code=500, detail="Haber güncellenemedi")
        
        return updated_haber
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"AI işleme hatası: {str(e)}"
        )


@router.get("/ai/status/{haber_id}")
def get_ai_status(
    haber_id: int,
    db: Session = Depends(get_db)
):
    """
    Haberin AI işlenme durumunu kontrol et
    
    Returns:
        {
            "haber_id": 4,
            "ai_islendi": 1,
            "has_flash_ozet": true,
            "has_detayli_ozet": true,
            "has_sentiment": true,
            "has_keywords": true
        }
    """
    haber = db.query(Haber).filter(Haber.id == haber_id).first()
    
    if not haber:
        raise HTTPException(status_code=404, detail="Haber bulunamadı")
    
    return {
        "haber_id": haber.id,
        "ai_islendi": haber.ai_islendi,
        "has_flash_ozet": bool(haber.flash_ozet),
        "has_detayli_ozet": bool(haber.detayli_ozet),
        "has_sentiment": haber.sentiment_skor is not None,
        "has_keywords": bool(haber.anahtar_kelimeler)
    }


@router.post("/ai/batch-process")
def batch_process_haberler(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """
    Toplu AI işleme - İşlenmemiş haberleri işle
    
    - **limit**: Kaç haber işlenecek (max 10)
    
    İşlenmemiş haberleri (ai_islendi=0) bulur ve AI ile işler.
    """
    if limit > 10:
        limit = 10
    
    # İşlenmemiş haberleri getir
    unprocessed = db.query(Haber).filter(
        Haber.ai_islendi == 0,
        Haber.tam_metin.isnot(None),
        Haber.yayinda == 1
    ).limit(limit).all()
    
    if not unprocessed:
        return {
            "message": "İşlenecek haber yok",
            "processed": 0,
            "failed": 0
        }
    
    processed_count = 0
    failed_count = 0
    results = []
    
    for haber in unprocessed:
        try:
            # AI ile işle
            ai_result = ai_service.process_haber(
                tam_metin=haber.tam_metin,
                baslik=haber.baslik
            )
            
            # Güncelle
            haber_update = HaberUpdate(
                flash_ozet=ai_result["flash_ozet"],
                detayli_ozet=ai_result["detayli_ozet"],
                sentiment_skor=ai_result["sentiment_skor"],
                sentiment_label=ai_result["sentiment_label"],
                anahtar_kelimeler=ai_result["anahtar_kelimeler"],
                ai_islendi=1
            )
            
            HaberService.update(db, haber.id, haber_update)
            
            processed_count += 1
            results.append({
                "haber_id": haber.id,
                "baslik": haber.baslik[:50] + "...",
                "status": "success"
            })
            
        except Exception as e:
            failed_count += 1
            results.append({
                "haber_id": haber.id,
                "baslik": haber.baslik[:50] + "...",
                "status": "failed",
                "error": str(e)
            })
    
    return {
        "message": f"{processed_count} haber başarıyla işlendi, {failed_count} hata",
        "processed": processed_count,
        "failed": failed_count,
        "results": results
    }
