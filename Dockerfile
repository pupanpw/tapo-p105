# ใช้ Python 3.10 เป็น base image
FROM python:3.10-slim

# ตั้งค่าตำแหน่งทำงานใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปยัง container
COPY requirements.txt /app/requirements.txt

# ติดตั้ง dependencies จาก requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมดจากโปรเจคไปยัง container
COPY . /app

# เปิดพอร์ตที่ Flask ใช้งาน
EXPOSE 5001

# รันแอป Flask
CMD ["python", "app.py"]
