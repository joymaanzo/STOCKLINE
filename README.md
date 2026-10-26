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