# Media monitoring telegram bot

## Requirements
python3.8 + poetry, mongodb >= 4.4
## Usage
```bash
poetry install --no-dev
poetry run python -m media_monitoring [OPTIONS]
```

## Options
```
-o --offset          start with an offset, in seconds
-t --timeout         interval, in seconds
-e --env-file        path to env file
```

## Env file
```bash
DEBUG
DATABASE_URL
DATABASE_NAME
TELEGRAM_API_TOKEN
```