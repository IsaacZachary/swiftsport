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

## Deploy on the MobKazi VPS (Ubuntu, nginx, Postgres)

```bash
# 1. Code and Python
sudo git clone https://github.com/IsaacZachary/swiftsport /srv/swiftsport
cd /srv/swiftsport
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt

# 2. Database
sudo -u postgres psql -c "CREATE USER swiftsport WITH PASSWORD 'pick-a-strong-password';"
sudo -u postgres psql -c "CREATE DATABASE swiftsport OWNER swiftsport;"

# 3. Settings: copy, then edit SECRET_KEY, DB password and domain
sudo cp .env.example .env && sudo nano .env
#    SECRET_KEY: python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# 4. Set up the database, files and logins
sudo .venv/bin/python manage.py migrate
sudo .venv/bin/python manage.py collectstatic --noinput
sudo .venv/bin/python manage.py import_seed
sudo .venv/bin/python manage.py createsuperuser          # your MobKazi login
sudo .venv/bin/python manage.py create_shop_manager wanyama   # prints his temporary password
sudo mkdir -p media && sudo chown -R www-data:www-data /srv/swiftsport

# 5. App server and web server (change port 8001 if another site uses it)
sudo cp deploy/swiftsport.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now swiftsport
sudo cp deploy/nginx-swiftsport.conf /etc/nginx/sites-available/swiftsport
sudo ln -s /etc/nginx/sites-available/swiftsport /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 6. HTTPS (after the domain points to the VPS)
sudo certbot --nginx -d swiftsport.co.ke -d www.swiftsport.co.ke
```

## Updating the site later

```bash
cd /srv/swiftsport && sudo git pull
sudo .venv/bin/pip install -r requirements.txt
sudo .venv/bin/python manage.py migrate
sudo .venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart swiftsport
```

Back up the database (`pg_dump swiftsport`) and the `media/` folder regularly: they hold everything Wanyama adds.
