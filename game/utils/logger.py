import logging

logging.basicConfig(
    filename="wildshade.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_info(message: str) -> None:
    logging.info(message)


def log_warning(message: str) -> None:
    logging.warning(message)


def log_error(message: str) -> None:
    logging.error(message)


def truncate_log(filename="wildshade.log") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.truncate()
