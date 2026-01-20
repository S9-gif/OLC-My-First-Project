from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..schemas.haber import (
    HaberCreate,
    HaberResponse,
    HaberUpdate,
    HaberListResponse
)
from ..services.haber_service import HaberService

router = APIRouter()


@router.post("/haberler", response_model=HaberResponse, status_code=201)
def create_haber(
    haber: HaberCreate,
    db: Session = Depends(get_db)
):
    """Yeni haber ekle (N8N kullanacak)"""
    return HaberService.create(db, haber)


@router.get("/haberler", response_model=HaberListResponse)
def list_haberler(
    kategori: Optional[str] = Query(None, description="spor, teknoloji, borsa, kitap"),
    sentiment: Optional[str] = Query(None, description="olumlu, nötr, olumsuz"),
    page: int = Query(1, ge=1, description="Sayfa numarası"),
    page_size: int = Query(20, ge=1, le=100, description="Sayfa başına kayıt"),
    db: Session = Depends(get_db)
):
    """Haberler listesi (Frontend kullanacak)"""
    skip = (page - 1) * page_size
    
    haberler = HaberService.get_list(
        db,
        kategori=kategori,
        sentiment=sentiment,
        skip=skip,
        limit=page_size
    )
    
    total = HaberService.count(db, kategori=kategori, sentiment=sentiment)
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "haberler": haberler
    }


@router.get("/haberler/{haber_id}", response_model=HaberResponse)
def get_haber(
    haber_id: int,
    db: Session = Depends(get_db)
):
    """Tek haber detayı"""
    haber = HaberService.get_by_id(db, haber_id)
    if not haber:
        raise HTTPException(status_code=404, detail="Haber bulunamadı")
    return haber


@router.patch("/haberler/{haber_id}", response_model=HaberResponse)
def update_haber(
    haber_id: int,
    haber_update: HaberUpdate,
    db: Session = Depends(get_db)
):
    """Haber güncelle (AI servisi kullanacak)"""
    haber = HaberService.update(db, haber_id, haber_update)
    if not haber:
        raise HTTPException(status_code=404, detail="Haber bulunamadı")
    return haber


@router.delete("/haberler/{haber_id}")
def delete_haber(
    haber_id: int,
    db: Session = Depends(get_db)
):
    """Haber sil (soft delete)"""
    success = HaberService.delete(db, haber_id)
    if not success:
        raise HTTPException(status_code=404, detail="Haber bulunamadı")
    return {"message": "Haber silindi", "id": haber_id}


@router.get("/haberler/bugun/liste", response_model=List[HaberResponse])
def get_bugunun_haberleri(
    kategori: Optional[str] = Query(None, description="Kategori filtresi"),
    db: Session = Depends(get_db)
):
    """Bugünün haberleri"""
    return HaberService.get_bugun(db, kategori)


@router.get("/stats/sentiment")
def get_sentiment_stats(
    kategori: Optional[str] = Query(None, description="Kategori filtresi"),
    db: Session = Depends(get_db)
):
    """Sentiment istatistikleri"""
    return HaberService.get_sentiment_stats(db, kategori)
