FROM python:3.10-alpine

WORKDIR /app

RUN pip install fastapi[standard]

EXPOSE 8002

COPY . .
ENTRYPOINT ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
