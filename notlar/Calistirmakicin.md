xampp aç (Apache + MySQL başlat)

.\venv\Scripts\python.exe -m uvicorn main:app --port 8081 --reload

1. Sandığı aç   → Activate.ps1
2. Sunucuyu başlat → uvicorn main:app ...

http://127.0.0.1:8081/giris   => giriş sayfası
http://127.0.0.1:8081/        => ana sayfa
http://127.0.0.1:8081/docs    => swagger API

NOT: 8080 portu başka bir uygulama tarafından kalıcı bloklu, 8081 kullanıyoruz