FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

RUN pip install --no-cache-dir --upgrade pip
RUN useradd -ms /bin/bash worker 
USER worker

WORKDIR /app/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker ./app /app
RUN pip install --no-cache-dir --user -r requirements.txt

