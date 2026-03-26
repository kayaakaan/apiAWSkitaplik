# veritabanı yapısını tanımlayan sayfa

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Text # Sütun Tİpleri
from sqlalchemy.orm import relationship # Tablolar arası İlişkiler
from database import Base # Veritabanı bağlantısı ve oturum yönetimi
# az önce database.py'de yazdığımız temel sınıf, buraya bağlanıyoruz
import datetime # Tarih için 
#üyelik tarihi, ödünç tarihi gibi alanlar için

class Kitap(Base):
    __tablename__ = "kitaplar" # Tablo adı

    id = Column(Integer, primary_key=True, index=True) # Otomatik artan ID
    # id adında bir sütun oluştur, tipi Integer olsun, primary key olsun, indexlensin

    baslik = Column(String(255), nullable=False) # Kitap başlığı Boş bırakılamaz
    yazar = Column(String(255), nullable=False) # Yazar adı Boş bırakılamaz
    isbn = Column(String(20), unique=True, nullable=False) # ISBN numarası Benzersiz ve boş bırakılamaz
    tur = Column(String(100), nullable=False) # Kitap türü Boş bırakılamaz
    yayin_yili = Column(Integer, nullable=False) # Yayın yılı Boş bırakılamaz
    adet = Column(Integer, default=1) # Kitap adedi Varsayılan 1
    aciklama = Column(Text, nullable=True) # Kitap açıklaması

    odunc_islemleri = relationship("OduncIslemi", back_populates="kitap") # Kitap ile ödünç işlemleri ilişkisi

# class Kitap(Base) → Base'den türetiyoruz, SQLAlchemy bunu otomatik tabloya çevirir
# __tablename__ → MySQL'de hangi tabloya karşılık geldiğini söyler
# nullable=False → bu alan boş bırakılamaz
# unique=True → aynı ISBN iki kere girilemez
# relationship → bu kitabın ödünç işlemleriyle bağlantısını kurar, ileride OduncIslem sınıfını yazınca anlam kazanır


class Uye(Base):
    __tablename__ = "uyeler" # Tablo adı

    id = Column(Integer, primary_key=True, index=True) # Otomatik artan ID
    ad = Column(String(100), nullable=False) # Üye adı Boş bırakılamaz
    soyad = Column(String(100), nullable=False) # Üye soyadı Boş bırakılamaz
    email = Column(String(255), unique=True, nullable=False) # E-posta Benzersiz ve boş bırakılamaz
    telefon = Column(String(20), nullable=True) # Telefon numarası
    uyelik_tarihi = Column(Date, default=datetime.date.today) # Üyelik tarihi Varsayılan bugünün tarihi
    aktif = Column(Boolean, default=True) # Üyelik aktif mi? Varsayılan aktif
    sifre = Column(String(255), nullable=False)  # Hashlenmiş şifre
    
    odunc_islemleri = relationship("OduncIslemi", back_populates="uye") # Üye ile ödünç işlemleri ilişkisi

# Date tipi kullandık → tarih saklamak için
# Boolean tipi kullandık → üye aktif mi değil mi (True/False)
# datetime.date.today → üye eklendiği gün otomatik yazılır, elle girmene gerek yok


class OduncIslemi(Base):
    __tablename__ = "odunc_islemleri" # Tablo adı

    id = Column(Integer, primary_key=True, index=True) # Otomatik artan ID
    kitap_id = Column(Integer, ForeignKey("kitaplar.id"), nullable=False) # Hangi kitap ödünç alındı? Boş bırakılamaz
    uye_id = Column(Integer, ForeignKey("uyeler.id"), nullable=False) # Hangi üye ödünç aldı? Boş bırakılamaz
    odunc_tarihi = Column(Date, default=datetime.date.today) # Ödünç alma tarihi Varsayılan bugünün tarihi
    iade_tarihi = Column(Date, nullable=True) # İade tarihi Boş olabilir
    iade_edildi = Column(Boolean, default=False) # Kitap iade edildi mi? Varsayılan hayır

    kitap = relationship("Kitap", back_populates="odunc_islemleri") # Ödünç işlemi ile kitap ilişkisi
    uye = relationship("Uye", back_populates="odunc_islemleri") # Ödünç işlemi ile üye ilişkisi

# ForeignKey("kitaplar.id") → bu sütun kitaplar tablosundaki id'ye bağlıdır, rastgele bir kitap ID'si yazamazsın
# ForeignKey("uyeler.id") → aynı şey üyeler için
# iade_tarihi boş başlar → kitap iade edilince doldurulur
# iade_edildi False başlar → iade edilince True olur
# relationship → hem kitaba hem üyeye bağlıdır, ikisini birbirine köprü gibi bağlar
