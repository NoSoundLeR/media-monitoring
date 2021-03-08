# Media rss monitoring bot

## Usage
```bash
poetry install --no-dev
poetry run python -m media_monitoring [OPTIONS]
```

## Options
```bash
-o --offset          start with an offset, in seconds
-t --timeout         interval, in seconds
```

## Env file
```bash
DATABASE_URL
DATABASE_NAME
TELEGRAM_API_TOKEN
```