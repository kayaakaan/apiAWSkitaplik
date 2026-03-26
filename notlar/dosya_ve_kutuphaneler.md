# 1. Sanal ortam oluştur : Projeye özel izole bir Python ortamı oluşturur. Yüklediğin kütüphaneler sadece bu projeye ait olur, bilgisayarının geneline karışmaz.
python -m venv venv

# 2. Sanal ortamı aktif et : O izole ortamı "aktif eder". Bundan sonra çalıştırdığın pip install komutları sisteme değil, bu klasöre yüklenir.
venv\Scripts\activate

# 3. Gerekli kütüphaneleri yükle
pip install fastapi uvicorn sqlalchemy pymysql cryptography python-dotenv "pydantic[email]"