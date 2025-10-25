# minimal, reproducible
# Note that this image of python is based on Linux Slim Debian
FROM python:3.10-slim

# avoid Python writing .pyc files & enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# install system deps (if required)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy dependency file first (build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app source
COPY src/ ./src

CMD ["sh", "-c", "/bin/bash"]