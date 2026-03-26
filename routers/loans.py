# ödünç işlemleriyle ilgili tüm endpoint'leri barındırır.



from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI araçları
from sqlalchemy.orm import Session                              # Veritabanı oturumu
from typing import List                                        # Liste tipi için

import model                # Veritabanı modelleri
import schemas              # Pydantic şemaları
import datetime
from database import get_db   # Veritabanı bağlantısı

router = APIRouter(prefix="/odunc", tags=["OduncIslemleri"])
# prefix → tüm endpoint'ler /odunc ile başlar
# tags  → Swagger'da gruplandırma için


# Tüm ödünç işlemlerini listele
@router.get("/", response_model=List[schemas.OduncResponse])
def tum_odunc_islemleri(db: Session = Depends(get_db)):
    odunc_islemleri = db.query(model.OduncIslemi).all()  # SELECT * FROM odunc
    return odunc_islemleri


# Sadece iade edilmemiş işlemleri listele
@router.get("/aktif", response_model=List[schemas.OduncResponse])
def aktif_islemler(db: Session = Depends(get_db)):
    islemler = db.query(model.OduncIslemi).filter(
        model.OduncIslemi.iade_edildi == False  # WHERE iade_edildi = False
    ).all()
    return islemler

# False	Kitap hâlâ dışarıda → aktif
# True	Kitap geri geldi → tamamlandı


# ID'ye göre ödünç işlemi getir
@router.get("/{islem_id}", response_model=schemas.OduncResponse)
def islem_getir(islem_id: int, db: Session = Depends(get_db)):
    islem = db.query(model.OduncIslemi).filter(model.OduncIslemi.id == islem_id).first()
    if not islem:
        raise HTTPException(status_code=404, detail="İşlem bulunamadı")
    return islem



# Kitap ödünç ver
@router.post("/", response_model=schemas.OduncResponse, status_code=status.HTTP_201_CREATED)
def kitap_odunc_ver(islem: schemas.OduncCreate, db: Session = Depends(get_db)):
    kitap = db.query(model.Kitap).filter(model.Kitap.id == islem.kitap_id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı") # Kitap yoksa hata döndür
    if kitap.adet < 1:
        raise HTTPException(status_code=400, detail="Kitabın mevcut adedi yok") # Kitap kalmamışsa hata döndür

    uye = db.query(model.Uye).filter(model.Uye.id == islem.uye_id).first()
    if not uye:  #  gönderilen üye ID'si veritabanında yoksa
        raise HTTPException(status_code=404, detail="Üye bulunamadı")
    if not uye.aktif: # üye pasifse ödünç veremezsin
        raise HTTPException(status_code=400, detail="Üye aktif değil")

    yeni_islem = model.OduncIslemi( # yeni bir ödünç işlemi oluştur
        kitap_id=islem.kitap_id,
        uye_id=islem.uye_id,
        odunc_tarihi=datetime.date.today(),  # Bugünün tarihi otomatik girer
    )
    kitap.adet -= 1  # Kitabın adetini 1 azalt
    db.add(yeni_islem)
    db.commit()
    db.refresh(yeni_islem)
    return yeni_islem


# Kitap iade al
@router.patch("/{islem_id}/iade", response_model=schemas.OduncResponse)
def kitap_iade_al(islem_id: int, db: Session = Depends(get_db)):
    islem = db.query(model.OduncIslemi).filter(model.OduncIslemi.id == islem_id).first()
    if not islem:
        raise HTTPException(status_code=404, detail="İşlem bulunamadı")
    if islem.iade_edildi:
        raise HTTPException(status_code=400, detail="Bu kitap zaten iade edilmiş")

    islem.iade_edildi = True                   # İade edildi olarak işaretle
    islem.iade_tarihi = datetime.date.today()  # İade tarihini bugün yap

    kitap = db.query(model.Kitap).filter(model.Kitap.id == islem.kitap_id).first()
    kitap.adet += 1  # Kitabın adetini 1 artır

    db.commit()
    db.refresh(islem)
    return islem

# Neden @router.patch kullandık, put değil?
# PUT → tüm nesneyi günceller
# PATCH → sadece bir kısmını günceller
