FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 9999

CMD ["sh", "-c", "sleep 5 && alembic upgrade head && uvicorn app:app --host 0.0.0.0 --port 9999"]