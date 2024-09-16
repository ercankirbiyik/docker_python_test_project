# Temel imajı belirle
FROM python:3.9-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt requirements.txt

# Gerekli Python bağımlılıklarını yükle
RUN pip install -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Testleri çalıştır
CMD ["pytest"]
