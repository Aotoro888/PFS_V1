# Dockerfile สำหรับ PFS V1.1
FROM python:3.10-slim

# ติดตั้ง tesseract และ dependencies ที่จำเป็น
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# คัดลอก requirements.txt แล้วติดตั้งไลบรารี
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมดไปใน container
COPY . /app
WORKDIR /app

# Run FastAPI app ด้วย Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
