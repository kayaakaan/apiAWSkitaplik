# books.py → kitaplarla ilgili tüm API endpoint'lerini barındırır

from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI araçları
from sqlalchemy.orm import Session                              # Veritabanı oturumu
from typing import List                                        # Liste tipi için

import model                # Veritabanı modelleri
import schemas              # Pydantic şemaları
from database import get_db   # Veritabanı bağlantısı

router = APIRouter(prefix="/kitaplar", tags=["Kitaplar"])
# prefix → tüm endpoint'ler /kitaplar ile başlar
# tags  → Swagger'da gruplandırma için


# TÜM KİTAPLARI GETİRME ENDPOINT'İ
@router.get("/", response_model=List[schemas.KitapResponse])
def kitaplari_getir(db: Session = Depends(get_db)):
    kitaplar = db.query(model.Kitap).all() # Tüm kitapları veritabanından çek
    return kitaplar # Pydantic şemasına göre otomatik dönüşüm yapılır

# @router.get("/") → GET /kitaplar/ adresine istek gelince bu fonksiyon çalışır
# response_model=List[schemas.KitapResponse] → cevap olarak KitapResponse listesi döner, Pydantic kontrol eder
# db: Session = Depends(get_db) → database.py'deki get_db fonksiyonunu çağırır, bize oturum verir
# db.query(model.Kitap).all() → SQL'deki SELECT * FROM kitaplar ile aynı şey


# ID YE GÖRE KİTAP GETİRME ENDPOINT'İ
@router.get("/{kitap_id}", response_model=schemas.KitapResponse)
def kitap_getir(kitap_id: int, db: Session = Depends(get_db)):
    kitap = db.query(model.Kitap).filter(model.Kitap.id == kitap_id).first() # ID'ye göre kitap bul
    if not kitap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kitap bulunamadı") # Kitap yoksa 404 hatası
    return kitap # Bulunan kitabı döndür

# /{kitap_id} → URL'den dinamik değer alır, mesela GET /kitaplar/5 gelince kitap_id = 5 olur
# .filter(model.Kitap.id == kitap_id) → SQL'deki WHERE id = 5 ile aynı
# .first() → ilk eşleşeni getir, yoksa None döner
# if not kitap → None döndüyse yani kitap bulunamadıysa...
# raise HTTPException(status_code=404) → kullanıcıya "404 Bulunamadı" hatası gönder


# KİTAP EKLEME ENDPOINT'İ
@router.post("/", response_model=schemas.KitapResponse, status_code=status.HTTP_201_CREATED)
def kitap_ekle(kitap: schemas.KitapCreate, db: Session = Depends(get_db)):
    mevcut = db.query(model.Kitap).filter(model.Kitap.isbn == kitap.isbn).first() # Aynı ISBN'li kitap var mı kontrol et
    if mevcut:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu ISBN'li kitap zaten var") # Varsa 400 hatası
    yeni_kitap = model.Kitap(**kitap.dict()) # Pydantic modelini SQLAlchemy modeline dönüştür
    db.add(yeni_kitap) # Yeni kitabı veritabanına ekle
    db.commit() # Değişiklikleri kaydet
    db.refresh(yeni_kitap) # Yeni kitabın ID'sini ve diğer otomatik alanları güncelle
    return yeni_kitap # Eklenen kitabı döndür          

# @router.post("/") → POST /kitaplar/ adresine istek gelince çalışır
# status_code=201 → başarılı eklemede 200 değil 201 Created döner
# kitap: schemas.KitapCreate → kullanıcının gönderdiği veriyi Pydantic ile doğrular
# mevcut kontrolü → aynı ISBN'li kitap varsa ekleme, 400 Bad Request hata ver
# **kitap.model_dump() → Pydantic nesnesini Python sözlüğüne çevirip Kitap modeline aktar
# db.add → ekle, db.commit → kaydet, db.refresh → ID'sini öğren        



# KİTAP GÜNCELLEME ENDPOINT'İ
@router.put("/{kitap_id}", response_model=schemas.KitapResponse)
def kitap_guncelle(kitap_id: int, guncelleme: schemas.KitapCreate, db: Session = Depends(get_db)):
    kitap = db.query(model.Kitap).filter(model.Kitap.id == kitap_id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    for alan, deger in guncelleme.model_dump().items():  # Her alanı tek tek güncelle
        setattr(kitap, alan, deger)

    db.commit()       # Kaydet
    db.refresh(kitap) # Güncel halini al
    return kitap

# @router.put("/{kitap_id}") → PUT /kitaplar/5 gelince ID'si 5 olan kitabı güncelle
# for alan, deger in guncelleme.model_dump().items() → gelen tüm alanları döngüyle gez
# setattr(kitap, alan, deger) → her alanı tek tek güncelle, mesela kitap.baslik = "Yeni Başlık"



# KİTAP SİLME ENDPOINT'İ
@router.delete("/{kitap_id}", status_code=status.HTTP_204_NO_CONTENT)
def kitap_sil(kitap_id: int, db: Session = Depends(get_db)):
    kitap = db.query(model.Kitap).filter(model.Kitap.id == kitap_id).first()
    if not kitap:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı")

    # Bu kitaba ait ödünç kaydı var mı kontrol et
    odunc_var = db.query(model.OduncIslemi).filter(model.OduncIslemi.kitap_id == kitap_id).first()
    if odunc_var:
        raise HTTPException(status_code=400, detail="Bu kitaba ait ödünç kaydı var, önce ödünç kayıtlarını silin")

    db.delete(kitap)  # Sil
    db.commit()       # Kaydet

# @router.delete("/{kitap_id}") → DELETE /kitaplar/5 gelince ID'si 5 olan kitabı sil
# status_code=204 → başarılı silmede cevap gövdesi dönmez, sadece 204 No Content döner
# db.delete(kitap) → SQL'deki DELETE FROM kitaplar WHERE id=5 ile aynı

