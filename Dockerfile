FROM python:3.12-slim
WORKDIR /app

# Keep Python deterministic & quiet
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Upgrade pip to a fixed version before installing deps (fixes CVE-2025-8869)
COPY app/requirements.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip==25.3 \
 && pip install --no-cache-dir -r requirements.txt

# Copy app and run
COPY app/ ./
EXPOSE 8080
CMD ["gunicorn", "main:app", "-c", "gunicorn.conf.py"]
