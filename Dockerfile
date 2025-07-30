FROM python:3.10-slim

WORKDIR /app

# Sistem gereksinimleri
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı kopyala
COPY ./app ./app

# Uvicorn ile başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
