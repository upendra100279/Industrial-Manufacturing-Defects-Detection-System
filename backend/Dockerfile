FROM python:3.11-slim

# Install gcc and build tools needed by some packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install CPU-only torch first separately — much smaller than GPU version
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    torch==2.4.1+cpu \
    torchvision==0.19.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p storage/uploads storage/processed storage/weights storage/logs

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]