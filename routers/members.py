# Kullanılıclar ile ilgili endpoint'ler bu dosyada olacak

from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI araçları
from sqlalchemy.orm import Session                              # Veritabanı oturumu
from typing import List                                        # Liste tipi için

import model                # Veritabanı modelleri
import schemas              # Pydantic şemaları
import bcrypt                # Şifre hashleme için
from database import get_db   # Veritabanı bağlantısı

router = APIRouter(prefix="/uyeler", tags=["Uyeler"])
# prefix → tüm endpoint'ler /uyeler ile başlar
# tags  → Swagger'da gruplandırma için


# Tüm üyeleri listele
@router.get("/", response_model=List[schemas.UyeResponse])  # Tüm üyeleri listele
def tum_uyeler(db: Session = Depends(get_db)):
    uyeler = db.query(model.Uye).all()  # SELECT * FROM uyeler
    return uyeler


# Belirli bir üyeyi getir
@router.get("/{uye_id}", response_model=schemas.UyeResponse)   # GET /uyeler/3 → ID'si 3 olan üyeyi getir
def uye_getir(uye_id: int, db: Session = Depends(get_db)):
    uye = db.query(model.Uye).filter(model.Uye.id == uye_id).first()   # İlk eşleşeni al, yoksa None döner
    if not uye:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Üye bulunamadı")  # Üye yoksa hata döndür
    return uye


# Yeni üye ekle
@router.post("/", response_model=schemas.UyeResponse, status_code=status.HTTP_201_CREATED) #POST /uyeler/ → yeni üye ekle
def uye_ekle(uye: schemas.UyeCreate, db: Session = Depends(get_db)):
    mevcut = db.query(model.Uye).filter(model.Uye.email == uye.email).first()
    if mevcut:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı") # Varsa "zaten kayıtlı" değeri döndür
    sifre_hash = bcrypt.hashpw(uye.sifre.encode("utf-8"), bcrypt.gensalt()).decode("utf-8") # Şifreyi hashle
    uye_verisi = uye.model_dump() # Pydantic modelini dict'e çevir
    uye_verisi["sifre"] = sifre_hash # Hashlenmiş şifreyi dict'e ekle
    yeni_uye = model.Uye(**uye_verisi) # Gelen veriyi Uye nesnesine çevir
    db.add(yeni_uye)
    db.commit() # Veritabanına yaz ve kaydet
    db.refresh(yeni_uye) # Kaydedilen nesneyi (ID dahil) geri al
    return yeni_uye


# Üye bilgilerini güncelle
@router.put("/{uye_id}", response_model=schemas.UyeResponse)
def uye_guncelle(uye_id: int, guncelleme: schemas.UyeCreate, db: Session = Depends(get_db)):
    uye = db.query(model.Uye).filter(model.Uye.id == uye_id).first()
    if not uye:
        raise HTTPException(status_code=404, detail="Üye bulunamadı")
    for alan, deger in guncelleme.model_dump().items(): # Gelen tüm alanları döngüyle gezerek güncelle
        setattr(uye, alan, deger)
    db.commit() # Veritabanına yaz ve kaydet
    db.refresh(uye) # Güncellenen nesneyi geri al
    return uye



# Üye sil
@router.delete("/{uye_id}", status_code=status.HTTP_204_NO_CONTENT)
def uye_sil(uye_id: int, db: Session = Depends(get_db)):
    uye = db.query(model.Uye).filter(model.Uye.id == uye_id).first() # Söylenen üye var mı kontrol et
    if not uye:
        raise HTTPException(status_code=404, detail="Üye bulunamadı")

    # Bu üyeye ait ödünç kaydı var mı kontrol et
    odunc_var = db.query(model.OduncIslemi).filter(model.OduncIslemi.uye_id == uye_id).first()
    if odunc_var:
        raise HTTPException(status_code=400, detail="Bu üyeye ait ödünç kaydı var, önce ödünç kayıtlarını silin")

    db.delete(uye) # Sil
    db.commit() # veri tabanına yaz ve kaydet
    # 204 döner → silindi, cevap gövdesi yok
