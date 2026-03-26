    # Postman API Rehberi

Base URL: `http://16.170.223.110`

---

## KİTAPLAR

### Tüm kitapları listele
- **Method:** GET
- **URL:** `http://16.170.223.110/kitaplar/`

---

### Tek kitap getir
- **Method:** GET
- **URL:** `http://16.170.223.110/kitaplar/1`
> URL'deki `1` yerine istediğin kitap ID'sini yaz

---

### Yeni kitap ekle
- **Method:** POST
- **URL:** `http://16.170.223.110/kitaplar/`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "baslik": "Suç ve Ceza",
    "yazar": "Fyodor Dostoyevski",
    "isbn": "978-975-123-456-7",
    "tur": "Roman",
    "yayin_yili": 1866,
    "adet": 3,
    "aciklama": "Klasik Rus edebiyatı"
}
```

---

### Kitap güncelle
- **Method:** PUT
- **URL:** `http://16.170.223.110/kitaplar/1`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "baslik": "Suç ve Ceza",
    "yazar": "Fyodor Dostoyevski",
    "isbn": "978-975-123-456-7",
    "tur": "Roman",
    "yayin_yili": 1866,
    "adet": 5,
    "aciklama": "Güncellendi"
}
```

---

### Kitap sil
- **Method:** DELETE
- **URL:** `http://16.170.223.110/kitaplar/1`

---

## ÜYELER

### Tüm üyeleri listele
- **Method:** GET
- **URL:** `http://16.170.223.110/uyeler/`

---

### Tek üye getir
- **Method:** GET
- **URL:** `http://16.170.223.110/uyeler/1`

---

### Yeni üye ekle
- **Method:** POST
- **URL:** `http://16.170.223.110/uyeler/`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "ad": "Ahmet",
    "soyad": "Yılmaz",
    "email": "ahmet@mail.com",
    "telefon": "05551234567",
    "sifre": "123456"
}
```

---

### Üye güncelle
- **Method:** PUT
- **URL:** `http://16.170.223.110/uyeler/1`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "ad": "Ahmet",
    "soyad": "Yılmaz",
    "email": "ahmet@mail.com",
    "telefon": "05559999999",
    "sifre": "123456"
}
```

---

### Üye sil
- **Method:** DELETE
- **URL:** `http://16.170.223.110/uyeler/1`

---

## ÖDÜNÇ İŞLEMLERİ

### Tüm ödünç işlemlerini listele
- **Method:** GET
- **URL:** `http://16.170.223.110/odunc/`

---

### Sadece aktif (iade edilmemiş) ödünçleri listele
- **Method:** GET
- **URL:** `http://16.170.223.110/odunc/aktif`

---

### Yeni ödünç işlemi oluştur
- **Method:** POST
- **URL:** `http://16.170.223.110/odunc/`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "kitap_id": 1,
    "uye_id": 1
}
```

---

### Kitabı iade al
- **Method:** PATCH
- **URL:** `http://16.170.223.110/odunc/1/iade`
> URL'deki `1` yerine ödünç işleminin ID'sini yaz

---

## GİRİŞ

### Üye girişi yap
- **Method:** POST
- **URL:** `http://16.170.223.110/giris/dogrula`
- **Headers:** `Content-Type: application/json`
- **Body → raw → JSON:**
```json
{
    "ad": "Ahmet",
    "sifre": "123456"
}
```

**Başarılı cevap (200):**
```json
{
    "basarili": true,
    "mesaj": "Hoş geldin, Ahmet Yılmaz!"
}
```

**Hatalı cevap — şifre yanlışsa (401):**
```json
{
    "detail": "Şifre hatalı"
}
```

**Hatalı cevap — üye bulunamazsa (401):**
```json
{
    "detail": "Kullanıcı bulunamadı"
}
```

> NOT: Önce `POST /uyeler/` ile şifreli üye ekle, sonra aynı ad ve şifreyle giriş yap.

---

## Postman'de Body Nasıl Ayarlanır?

POST ve PUT istekleri için:
1. İsteği seç → **Body** sekmesine tıkla
2. **raw** seçeneğini işaretle
3. Sağdaki dropdown'dan **JSON** seç
4. JSON verisini yaz ve **Send** butonuna bas
