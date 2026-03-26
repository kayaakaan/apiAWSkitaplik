from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from routers import books, members, loans
import model
import bcrypt
import os

from fastapi.responses import FileResponse

# Veritabanı tablolarını otomatik oluştur (yoksa)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kitaplık Yönetim Sistemi API",
    description="Kitap, üye ve ödünç işlemlerini yöneten REST API",
    version="1.0.0",
)

@app.get("/")
async def read_index():
    return FileResponse("static/login.html")

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)

@app.get("/")
def ana_sayfa():
    return FileResponse("static/login.html")

@app.get("/giris")
def giris_sayfasi():
    return FileResponse("static/login.html")

@app.get("/uye-ekle")
def uye_ekle_sayfasi():
    return FileResponse("static/uye-ekle.html")

@app.get("/kitap-ekle")
def kitap_ekle_sayfasi():
    return FileResponse("static/kitap-ekle.html")

@app.get("/odunc")
def odunc_sayfasi():
    return FileResponse("static/odunc.html")

@app.post("/giris/dogrula")
def giris_dogrula(veri: dict, db: Session = Depends(get_db)):
    ad = veri.get("ad", "").strip()
    sifre = veri.get("sifre", "")
    if not ad or not sifre:
        raise HTTPException(status_code=400, detail="Ad ve şifre boş olamaz")
    uye = db.query(model.Uye).filter(
        model.Uye.ad == ad,
        model.Uye.aktif == True
    ).first()
    if not uye:
        raise HTTPException(status_code=401, detail="Giriş yapılamadı")
    if not uye.sifre:
        raise HTTPException(status_code=401, detail="Giriş yapılamadı")
    if not bcrypt.checkpw(sifre.encode("utf-8"), uye.sifre.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Giriş yapılamadı")
    return {"basarili": True, "mesaj": f"Hoş geldin, {uye.ad} {uye.soyad}!"}


