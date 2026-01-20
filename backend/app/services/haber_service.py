from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta

from ..models.haber import Haber
from ..schemas.haber import HaberCreate, HaberUpdate


class HaberService:
    """Haber CRUD operations ve business logic"""
    
    @staticmethod
    def create(db: Session, haber: HaberCreate) -> Haber:
        """Yeni haber oluştur (N8N kullanacak)"""
        db_haber = Haber(**haber.model_dump())
        db.add(db_haber)
        db.commit()
        db.refresh(db_haber)
        return db_haber
    
    @staticmethod
    def get_by_id(db: Session, haber_id: int) -> Optional[Haber]:
        """ID'ye göre haber getir ve okunma sayısını artır"""
        haber = db.query(Haber).filter(Haber.id == haber_id).first()
        if haber:
            haber.okunma_sayisi += 1
            db.commit()
        return haber
    
    @staticmethod
    def get_list(
        db: Session,
        kategori: Optional[str] = None,
        sentiment: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Haber]:
        """Haberler listesi - filtreli ve sayfalı"""
        query = db.query(Haber).filter(Haber.yayinda == 1)
        
        if kategori:
            query = query.filter(Haber.kategori == kategori)
        
        if sentiment:
            query = query.filter(Haber.sentiment_label == sentiment)
        
        return query.order_by(desc(Haber.yayin_tarihi))\
                   .offset(skip)\
                   .limit(limit)\
                   .all()
    
    @staticmethod
    def count(
        db: Session,
        kategori: Optional[str] = None,
        sentiment: Optional[str] = None
    ) -> int:
        """Toplam haber sayısı"""
        query = db.query(Haber).filter(Haber.yayinda == 1)
        
        if kategori:
            query = query.filter(Haber.kategori == kategori)
        
        if sentiment:
            query = query.filter(Haber.sentiment_label == sentiment)
        
        return query.count()
    
    @staticmethod
    def update(db: Session, haber_id: int, haber_data: HaberUpdate) -> Optional[Haber]:
        """Haber güncelle (AI servisi kullanacak)"""
        haber = db.query(Haber).filter(Haber.id == haber_id).first()
        if not haber:
            return None
        
        for key, value in haber_data.model_dump(exclude_unset=True).items():
            setattr(haber, key, value)
        
        db.commit()
        db.refresh(haber)
        return haber
    
    @staticmethod
    def delete(db: Session, haber_id: int) -> bool:
        """Haber sil (soft delete)"""
        haber = db.query(Haber).filter(Haber.id == haber_id).first()
        if not haber:
            return False
        
        haber.yayinda = 0
        db.commit()
        return True
    
    @staticmethod
    def get_bugun(db: Session, kategori: Optional[str] = None) -> List[Haber]:
        """Bugünün haberleri"""
        bugun = datetime.now().date()
        query = db.query(Haber).filter(
            Haber.yayinda == 1,
            func.date(Haber.yayin_tarihi) == bugun
        )
        
        if kategori:
            query = query.filter(Haber.kategori == kategori)
        
        return query.order_by(desc(Haber.yayin_tarihi)).all()
    
    @staticmethod
    def get_sentiment_stats(db: Session, kategori: Optional[str] = None) -> dict:
        """Sentiment istatistikleri"""
        query = db.query(
            Haber.sentiment_label,
            func.count(Haber.id).label('count')
        ).filter(
            Haber.sentiment_label.isnot(None),
            Haber.yayinda == 1
        )
        
        if kategori:
            query = query.filter(Haber.kategori == kategori)
        
        results = query.group_by(Haber.sentiment_label).all()
        
        total = sum([r.count for r in results])
        
        stats = {}
        for r in results:
            stats[r.sentiment_label] = {
                "count": r.count,
                "percentage": round((r.count / total * 100), 2) if total > 0 else 0
            }
        
        return {
            "total": total,
            "breakdown": stats
        }
