FROM python:3.11-slim

# جلوگیری از نوشتن .pyc و تنظیم stdout بدون بافر
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب پیش‌نیازهای سیستمی برای psycopg2, bcrypt, cryptography و غیره
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway متغیر PORT رو ست می‌کنه
ENV PORT=8000
EXPOSE 8000

# اجرای سرور (می‌تونی gunicorn بذاری اگه خواستی)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
