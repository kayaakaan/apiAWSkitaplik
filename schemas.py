# API'ye gelen/giden verinin şeklini tanımlar

from pydantic import BaseModel, EmailStr # Veri doğrulaması için
from typing import Optional # zorunlu olmayan alanlar için
import datetime # Tarih için


# ── KİTAP SCHEMALARI ──────────────────────────

class KitapBase(BaseModel):
    # Hem eklerken hem güncellerken ortak olan alanlar
    baslik: str
    yazar: str
    isbn: str
    tur: Optional[str] = None # Zorunlu değil 
    yayin_yili: Optional[int] = None
    adet: int = 1
    aciklama: Optional[str] = None

class KitapCreate(KitapBase):
    # Kitap eklerken gereken alanlar, KitapBase'den alır
    pass 

class KitapResponse(KitapBase):
    # API cevap verirken kullanlılan, id de döner
    id: int
    model_config = {"from_attributes": True} # SQLAlchemy nesnelerini okuyabilmek için

# KitapBase	Ortak alanları bir yerde toplar
# KitapCreate	Kullanıcı yeni kitap eklerken gönderir (id yok, veritabanı üretir)
# KitapResponse	API cevap verirken döner (id dahil)


# ── ÜYE SCHEMALARI ────────────────────────────

class UyeBase(BaseModel):
    ad: str
    soyad: str
    email: EmailStr # E-posta formatında olmalı ==> test@gmail.com
    telefon: Optional[str] = None
    sifre: str  # Kullanıcının gireceği şifre

class UyeCreate(UyeBase):
    # Üye eklerken gereken alanlar, UyeBase'den alır
    pass

class UyeResponse(UyeBase):
    # API cevap verirken kullanılır
    id: int
    uyelik_tarihi: datetime.date # veritabanından gelir
    aktif: bool 

    model_config = {"from_attributes": True} # SQLAlchemy nesnelerini okuyabilmek için




# ── ÖDÜNÇ İŞLEM SCHEMALARI ────────────────────

class OduncIslemiBase(BaseModel):
    # Ödün. verirken sadece hangi kitap ve üye gönderir
    kitap_id: int # hangi kitap ID'si
    uye_id: int # hangi üye ID'si

class OduncCreate(OduncIslemiBase):
    # Ödünç verirken kullanılır
    pass

class OduncResponse(BaseModel):
    # API cevap verirken tüm bilgileri döner
    id: int
    kitap_id: int
    uye_id: int
    odunc_tarihi: datetime.date
    iade_tarihi: Optional[datetime.date] = None # iade tarihi boş olabilir
    iade_edildi: bool
    
    model_config = {"from_attributes": True} # SQLAlchemy nesnelerini okuyabilmek için