FROM python:3.12-slim

WORKDIR /weather

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY task-1.py .

EXPOSE 8000

CMD ["python", "task-1.py"]
