# depot_depo_employee_project

## Overview

Django application for managing employees, jobs, piecework payments, and materials. Supports filtering and export to Excel/PDF.

## Project structure

```
.
├── depo_crud/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── employee/
│   ├── templates/
│   ├── views/
│   ├── static/           # source static assets
│   └── ...
├── commando/             # management commands (incl. auto_admin)
├── static/               # project-level static sources
├── staticfiles/          # collectstatic output (do not commit)
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.prod.sh
├── package.json
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.13
- Node.js ≥20 (verify with package.json “engines”) and npm 10+
- MySQL 8+ (or compatible)

## Installation (development)

```sh
git clone <repository-url>
cd depot_depo_employee_project

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Frontend
npm ci
npm run build   # builds CSS/JS into static/dist
```

## Configuration (.env)

Create a .env file in the repo root (do not commit it). Provide either a URL or individual settings:

```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True

# Option A: single URL
MYSQL_PUBLIC_URL=mysql://user:pass@localhost:3306/dbname

# Option B: separate parts
MYSQL_DATABASE=dbname
MYSQL_USER=user
MYSQL_PASSWORD=pass
MYSQL_HOST=localhost
MYSQL_PORT=3306

ALLOWED_HOSTS=127.0.0.1,localhost
INTERNAL_IPS=127.0.0.1
```

Static settings: STATIC_ROOT=staticfiles, STATICFILES_DIRS includes “static” (see depo_crud/settings.py).

## Running (development)

```sh
python manage.py migrate
npm run dev   # Vite dev server (HMR), run in a separate terminal
python manage.py runserver
# open http://127.0.0.1:8000/
```

## Running (Docker)

```sh
docker compose up -d --build
# open http://127.0.0.1:8000/
```

Entrypoint (entrypoint.prod.sh) does:

- database wait
- `python manage.py migrate`
- `python manage.py auto_admin --force` (creates/ensures admin user)
- verifies static/dist assets exist
- `python manage.py collectstatic --noinput`
- starts Gunicorn

Security: change the admin credentials created by auto_admin immediately after first deploy.

Dev-only ports: keep port mappings in docker-compose.override.yml so production runs without exposed db/web ports by default.

## Static files

- Build source assets into `static/` with npm scripts (`dev` for the Vite dev server, `build` for a production build, `watch` to rebuild on save without a dev server).
- `collectstatic` writes to `staticfiles/` (runtime output, not committed).
- Before collectstatic, ensure `static/manifest.json` exists (produced by `npm run build`).

## Tests

```sh
python manage.py test
```

## Troubleshooting

- If entrypoint fails on Windows line endings, ensure LF (git config core.autocrlf=input) or see Dockerfile step normalizing CRLF.
- For slow builds, use BuildKit and lockfiles: `DOCKER_BUILDKIT=1 npm ci && docker buildx build ...`.

## License

MIT. Ensure a LICENSE file is present in the repository root.
