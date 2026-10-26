# STOCKLINE

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest
```

## Running with Docker

```bash
docker compose up --build
```

Open http://localhost:8000.

docker compose up --build starts the app and Postgres. In GitHub Codespaces, container-to-container traffic timed out (the app could not reach postgres:5432), so the app and Postgres were verified by publishing the Postgres port and running the app on the host: 25 tests passed against Postgres, /health returned {"status":"ok"}, and the watchlist_items table was created. Compose has not been verified end to end in Codespaces.

## Project

STOCKLINE is a JSE stock tracker for beginner investors and students. It helps users browse South African shares, inspect price movements, review a deterministic opportunity score, and manage a watchlist. It is an analysis and tracking tool, not a broker, and it does not execute trades.

The application currently uses labelled deterministic demo prices. Demo data is not live market data and must not be treated as investment advice.

## Tests

```bash
python -m pytest -q
```

## Render deployment

The Render Blueprint uses the Dockerfile and requires the `DATABASE_URL` environment variable to be configured in Render. No secret values are committed.

Deployed URL: `https://stockline-cx3t.onrender.com`

The deployed app uses a Render Postgres database via the `DATABASE_URL` environment variable (not committed to the repo), and a watchlist entry was verified to persist across a redeploy.

The Render free tier may sleep when idle, so the first request after inactivity can be slower or unavailable while the service wakes.

## Known limitations

The MVP implementation plan in `docs/mvp-spec.md` section 10 identifies work that is not complete in this release:

- Database migrations, provider research, caching, freshness handling, and provider fallbacks are not fully implemented.
- User accounts, authentication, and cross-user watchlist ownership are not implemented.
- Price alerts, scheduled polling, crossing detection, and email delivery are not implemented.
- AI explanations, fundamentals, structured risk prompts, and provider fallbacks are not implemented; analysis uses fixed rule-based text.
- Browser journey coverage, JSON logging, metrics beyond the health endpoint, and deployment smoke tests are limited.
- Hosted on Render's free tier, so the first request after idle can take about 50 seconds, and the free Postgres database expires after a limited period.