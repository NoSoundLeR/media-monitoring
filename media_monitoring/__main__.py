import argparse
import asyncio
import logging
import os

logging.basicConfig()
DEBUG = os.getenv("DEBUG") in (
    "1",
    "true",
    "True",
)
level = logging.DEBUG if DEBUG else logging.INFO
log = logging.getLogger("media")
log.setLevel(level)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--offset", type=int, default=0, help="monitoring offset in seconds"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=60, help="monitoring timeout"
    )
    parser.add_argument("-e", "--env-file", default=".env", help="path to env file")
    args = parser.parse_args()

    log.debug(f"offset: {args.offset}")
    log.debug(f"timeout: {args.timeout}")

    log.debug("Reading env file...")

    with open(args.env_file, "r") as f:
        for line in f.readlines():
            log.debug(line.strip())
            if line.startswith("#"):
                continue
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

    from media_monitoring.monitoring import run_monitoring
    from media_monitoring.telegram import start_bot

    loop = asyncio.get_event_loop()
    loop.create_task(run_monitoring(offset=args.offset, timeout=args.timeout))
    start_bot(loop)


if __name__ == "__main__":
    run()
