# Swift Sport

Website for Swift Sport / Tactical Gear, Embakasi, Nairobi. Built by MobKazi with Django.

- `/` is the shop page: products, prices, WhatsApp ordering, location and hours.
- `/admin/` is the shop manager: add, edit and delete products and photos, mark items out of stock, and change the phone, hours and location.
- `/api/products` returns the same data as JSON.

Photos uploaded in the admin are resized to 1200 px JPEGs automatically.

## Try it on your PC (Python 3.10+)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
echo DEBUG=true > .env
python manage.py migrate
python manage.py import_seed     # loads the 18 starting products and photos
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/admin/.

## Deploy on the MobKazi VPS (Docker behind Coolify's Traefik)

The VPS runs every MobKazi app in Docker. Coolify's Traefik proxy (`coolify-proxy`) owns ports 80/443,
routes each domain to its containers over the `mobkazi-network` Docker network and gets Let's Encrypt
certificates automatically. `docker-compose.yml` follows the same pattern: a Postgres container, the
Django app (gunicorn + WhiteNoise for static files) and a small nginx container that serves `/media/`.
No host ports are published, and Traefik picks the containers up without being restarted.

```bash
# 1. Code
git clone https://github.com/IsaacZachary/swiftsport /srv/swiftsport
cd /srv/swiftsport

# 2. Settings: SECRET_KEY, Postgres password and domain (see .env.example)
cp .env.example .env && nano .env && chmod 600 .env

# 3. Build and start (migrations run automatically when the web container starts)
docker compose up -d --build

# 4. Starting products and logins
docker compose exec web python manage.py import_seed
docker compose exec web python manage.py createsuperuser             # your MobKazi login
docker compose exec web python manage.py create_shop_manager wanyama # prints his temporary password
```

DNS: A records for `swiftsport.co.ke` and `www` point to 62.171.151.208. Traefik requests the
certificates by HTTP challenge, so they are issued once the domain resolves to the VPS. If the
containers were started before that, trigger a fresh attempt with
`docker compose up -d --force-recreate web media`. With Cloudflare's proxy (orange cloud) on, set
SSL/TLS mode to **Full (strict)**.

## Updating the site later

```bash
cd /srv/swiftsport && git pull
docker compose up -d --build
```

Back up the database and the photos regularly: they hold everything Wanyama adds.

```bash
docker compose exec -T db pg_dump -U swiftsport swiftsport > swiftsport-$(date +%F).sql
docker run --rm -v swiftsport_swiftsport-media:/m -v "$PWD":/b alpine tar czf /b/media-$(date +%F).tgz -C /m .
```
