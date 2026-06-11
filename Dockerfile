FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV LOCAL_MODEL_DIR=/tmp/mlops-pf-model

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY scripts ./scripts

EXPOSE 8080

CMD ["sh", "-c", "python scripts/download_artifacts.py && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
