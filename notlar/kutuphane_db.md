-- Kitaplar tablosu
CREATE TABLE kitaplar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    baslik VARCHAR(255) NOT NULL,
    yazar VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    tur VARCHAR(100),
    yayin_yili INT,
    adet INT DEFAULT 1,
    aciklama TEXT
);

-- Üyeler tablosu
CREATE TABLE uyeler (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad VARCHAR(100) NOT NULL,
    soyad VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    uyelik_tarihi DATE DEFAULT (CURRENT_DATE),
    aktif BOOLEAN DEFAULT TRUE
);

-- Ödünç işlemleri tablosu
CREATE TABLE odunc_islemler (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kitap_id INT NOT NULL,
    uye_id INT NOT NULL,
    odunc_tarihi DATE DEFAULT (CURRENT_DATE),
    iade_tarihi DATE,
    iade_edildi BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (kitap_id) REFERENCES kitaplar(id),
    FOREIGN KEY (uye_id) REFERENCES uyeler(id)
);