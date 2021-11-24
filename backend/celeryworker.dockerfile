FROM python:3.9

WORKDIR /app/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./app /app

RUN bash -c "pip install --no-cache-dir --upgrade pip; pip install --no-cache-dir -r requirements.txt"

COPY ./startup_scripts /startup_scripts
RUN chmod -R +x /startup_scripts

RUN useradd --system --group worker && chown -R worker /app /startup_scripts
USER worker

ENTRYPOINT ["/startup_scripts/entrypoint.sh"]