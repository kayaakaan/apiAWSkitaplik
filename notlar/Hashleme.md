Postman → POST /uyeler/
         ↓
    members.py devreye girer
         ↓
    bcrypt "123456" → "$2b$12$xK9..." yapar (hashleme)
         ↓
    hashlenmiş şifre veritabanına kaydedilir



Giriş Yaparken
Postman → POST /giris/dogrula
         ↓
    main.py devreye girer
         ↓
    bcrypt: "123456" ile "$2b$12$xK9..." karşılaştırır
         ↓
    eşleşirse → "Hoş geldin!"
    eşleşmezse → "Şifre hatalı
