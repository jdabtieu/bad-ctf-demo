FROM python:3.11-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

# Gunicorn will bind to 0.0.0.0 so Docker can expose it
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

