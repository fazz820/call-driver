# Call Driver Agency

A Django application that connects customers with professional drivers. It supports customer and driver registration, booking management, driver dashboards, services, and an admin panel.

## Tech Stack

- Django 5.2
- Python 3.11+
- SQLite (local) / PostgreSQL (production)
- Bootstrap 5 (via CDN)
- Deployed on Vercel (serverless WSGI)

## Project Structure

```
call_driver_agency/
├── accounts/          # Custom user model, registration, login, profiles
├── bookings/          # Booking creation, assignment, status tracking
├── services/          # Service catalog and categories
├── drivers/           # Driver profiles, vehicles, driver dashboard
├── dashboard/         # Customer and admin dashboards
├── core/              # Home, about, contact pages + site settings
├── static/            # CSS, JS, images, videos
├── templates/         # Shared base template + per-app templates
├── call_driver_agency/  # Project settings, URLs, WSGI/ASGI entrypoints
├── manage.py
├── requirements.txt
└── vercel.json
```

## Local Development

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations and start the server
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000

### Optional: seed admin user

```bash
python manage.py createsuperuser
```

## Deploying to Vercel

1. Push this repository to GitHub.
2. In Vercel, import the repository. Vercel auto-detects Django via `manage.py` and uses `call_driver_agency/wsgi.py` as the entrypoint.
3. Vercel automatically runs `collectstatic` during the build (because `STATIC_ROOT` is configured) and serves `/static/` from its CDN.
4. Configure the following environment variables in Vercel:

| Variable               | Value                                                              |
| ---------------------- | ------------------------------------------------------------------ |
| `DJANGO_SECRET_KEY`    | A long random string (e.g. from `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DJANGO_DEBUG`         | `False`                                                            |
| `DJANGO_ALLOWED_HOSTS` | `your-app.vercel.app` (comma-separated for multiple domains)       |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.vercel.app`                                      |
| `DATABASE_URL`         | A PostgreSQL connection string, e.g. `postgres://user:pass@host/db` from Neon, Supabase, or similar |

> Note: SQLite will not persist on Vercel's serverless infrastructure. Use the `DATABASE_URL` Postgres option in production.

5. After the first deploy, open the Vercel project, go to **Settings > Environment Variables** to add them, then deploy again.
6. Run migrations against your Postgres database once:

```bash
python manage.py migrate
```

### Important: file uploads

`MEDIA_ROOT` (`media/`) stores driver photos, license images, and service images/videos locally. On Vercel these uploads do not persist between requests. For production uploads, add a cloud storage backend such as Amazon S3, Cloudflare R2, or Cloudinary and wire it into Django's `STORAGES` settings.

## Notable configuration

- `AUTH_USER_MODEL = 'accounts.CustomUser'` — custom user with email login.
- `DATABASES` reads `DATABASE_URL` if present, otherwise falls back to a local SQLite file.
- `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG`, and `CSRF_TRUSTED_ORIGINS` are all controlled via environment variables.
