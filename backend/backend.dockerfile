FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app/
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./app /app

RUN bash -c "pip install --no-cache-dir --upgrade pip; pip install --no-cache-dir -r requirements.txt"