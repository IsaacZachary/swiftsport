FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
# Static files are baked into the image and served by WhiteNoise.
# Media (uploaded photos) lives in a volume owned by the unprivileged app user.
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput \
 && useradd --uid 10001 --create-home --shell /usr/sbin/nologin app \
 && mkdir -p /app/media && chown app /app/media

USER app
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn swiftsport.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60 --access-logfile -"]
