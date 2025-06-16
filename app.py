# app.py
import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Payment
from datetime import datetime
from PIL import Image
import pytesseract

# เชื่อมต่อ PostgreSQL (Render)
DATABASE_URL = "postgresql://praifahbot2_user:wR3l2D6iKolRbGizDHrEA2BEbeJTByRa@dpg-d179v40dl3ps73a7913g-a/praifahbot2"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# สร้างแอป
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# หน้าแรก
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    db = SessionLocal()
    payments = db.query(Payment).order_by(Payment.upload_time.desc()).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "payments": payments})

# อัปโหลดไฟล์
@app.post("/upload")
async def upload_file(
    request: Request,
    house_number: str = Form(...),
    month_year: str = Form(...),
    file: UploadFile = File(...)
):
    os.makedirs(f"uploads/{house_number}", exist_ok=True)
    filename = f"{month_year.replace('/', '_')}_{file.filename}"
    filepath = f"uploads/{house_number}/{filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # OCR ตรวจหา "300 บาท"
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image, lang="tha+eng")
    amount_verified = "300 บาท" in text

    # บันทึกลงฐานข้อมูล
    db = SessionLocal()
    payment = Payment(
        house_number=house_number,
        month_year=month_year,
        image_filename=filepath,
        amount_verified=amount_verified,
        upload_time=datetime.utcnow()
    )
    db.add(payment)
    db.commit()
    db.close()

    # แสดงผลลัพธ์
    db = SessionLocal()
    payments = db.query(Payment).order_by(Payment.upload_time.desc()).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "payments": payments, "message": "อัปโหลดสำเร็จ"})
