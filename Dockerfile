# Python image
FROM python:3.10-slim

# Working directoryni o'rnatamiz
WORKDIR /app

# Talablarni (dependencies) o'rnatish
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# .env faylini konteynerga nusxalash
COPY .env /app/.env

# Ilovani yuklash
COPY . /app

# Django statik fayllarni tayyorlash
RUN python manage.py collectstatic --noinput

# Portni ochish
EXPOSE 8000

# Django serverni ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
