# depot_depo_employee_project

## Overview

Django application for managing employees, jobs, piecework payments, and materials. Supports filtering and export to Excel/PDF.

## Project structure

```
.
├── depo_crud/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py        # DJANGO_SETTINGS_MODULE default for manage.py
│   │   ├── production.py   # DJANGO_SETTINGS_MODULE default for wsgi/asgi/Docker
│   │   └── test.py         # used in CI
│   ├── urls.py
│   └── wsgi.py
├── employee/
│   ├── templates/
│   ├── views/
│   ├── static/           # source static assets
│   └── ...
├── static/               # project-level static sources
├── staticfiles/          # collectstatic output (do not commit)
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── entrypoint.prod.sh
├── package.json
├── requirements.txt      # production dependencies
├── requirements-dev.txt  # linters, tests, debug toolbar
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

# requirements.txt is what the production image installs; the dev file adds
# linters, test tools and the debug toolbar on top.
pip install -r requirements.txt -r requirements-dev.txt

# Frontend
npm ci
npm run build   # builds CSS/JS into static/
```

## Configuration (.env)

Create a .env file in the repo root (do not commit it). Provide either a URL or individual settings:

```
DJANGO_SECRET_KEY=change-me

# Option A: single URL
MYSQL_PUBLIC_URL=mysql://user:pass@localhost:3306/dbname

# Option B: separate parts
MYSQL_DATABASE=dbname
MYSQL_USER=user
MYSQL_PASSWORD=pass
MYSQL_HOST=localhost
MYSQL_PORT=3306

# Only needed in production/CI - local.py hardcodes permissive defaults.
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://example.com

INTERNAL_IPS=127.0.0.1
NPM_BIN_PATH=/usr/local/bin/npm   # only if npm isn't on PATH

# Optional - defaults to console/SMTP backend depending on environment.
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=no-reply@example.com

# Optional, production only - error monitoring stays off until this is set.
SENTRY_DSN=
```

`DJANGO_SETTINGS_MODULE` picks the environment (`depo_crud.settings.local`/`.production`/`.test`) and must **not** be put in `.env` — `.env` is loaded from inside the settings module itself, after Python has already resolved which one to import. `manage.py` defaults to `.local` when unset; `wsgi.py`/`asgi.py`/the Dockerfile default to `.production`.

Static settings: STATIC_ROOT=staticfiles, STATICFILES_DIRS includes “static” (see depo_crud/settings/base.py).

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
- ensures an admin user exists (`manage.py createsuperuser --noinput`, skipped if one
  already exists) - requires `DJANGO_SUPERUSER_PASSWORD` in the environment. Log in
  with `admin@admin.com` (not `admin`) - a save-time signal syncs username to email,
  so that's the username that actually gets persisted
- verifies static/manifest.json exists
- `python manage.py collectstatic --noinput`
- starts Gunicorn

Security: change the admin password immediately after first deploy.

Order matters here: `collectstatic` must run before Gunicorn starts. django-vite
doesn't set an explicit `manifest_path`, so it defaults to reading
`STATIC_ROOT/manifest.json` - a file `collectstatic` creates, not one that
exists from image build. Render a template before that step ever runs and
`{% vite_asset %}` raises `DjangoViteAssetNotFoundError`.

Dev-only ports: keep port mappings in docker-compose.override.yml so production runs without exposed db/web ports by default.

## Static files

- Build source assets into `static/` with npm scripts (`dev` for the Vite dev server, `build` for a production build, `watch` to rebuild on save without a dev server).
- `collectstatic` writes to `staticfiles/` (runtime output, not committed).
- Before collectstatic, ensure `static/manifest.json` exists (produced by `npm run build`).

## Code style

Ruff (Python), Prettier (templates, CSS, TypeScript), djLint (template linting) and `tsc`
run automatically through pre-commit. Install the hooks once after `pip install`:

```sh
pre-commit install --hook-type pre-commit --hook-type pre-push
```

Both hook types are required: `tsc` checks the whole project at once, so it runs on push
rather than on every commit.

```sh
pre-commit run --all-files   # everything, as CI runs it
ruff check . && ruff format .
npm run typecheck
```

Who owns what: Prettier formats templates, djLint only lints them. The two cannot both
format — `djlint --reformat` and Prettier rewrite each other's output indefinitely.

Hook `rev` values for `ruff` and `djlint` in `.pre-commit-config.yaml` must match their
pins in `requirements-dev.txt`, or a manual run and the hook disagree. Prettier needs no
such pin: its hook runs from `node_modules`, so `npm ci` has to happen before
`pre-commit run` on a fresh checkout.

## Tests

```sh
DJANGO_SETTINGS_MODULE=depo_crud.settings.test python manage.py test
```

Runs against the same prod-shaped settings (`DEBUG=False`, manifest-backed static assets) as what's actually deployed, plus a fast password hasher and an in-memory email backend. The "Django: Tests" VS Code task already sets this.

## Troubleshooting

- If entrypoint fails on Windows line endings, ensure LF (git config core.autocrlf=input) or see Dockerfile step normalizing CRLF.
- For slow builds, use BuildKit and lockfiles: `DOCKER_BUILDKIT=1 npm ci && docker buildx build ...`.

## License

MIT. Ensure a LICENSE file is present in the repository root.
