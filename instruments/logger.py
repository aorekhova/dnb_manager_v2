import logging
from logging.handlers import RotatingFileHandler
import os
from contextlib import contextmanager

LOG_DIR = r"C:\analytics_scripts\scripts\dnb_manager\logs"
os.makedirs(LOG_DIR, exist_ok=True)

MAIN_LOG_FILE = os.path.join(LOG_DIR, "dnb_manager.log")

logger = logging.getLogger("dnb")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


main_file_handler = RotatingFileHandler(
    MAIN_LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)
main_file_handler.setFormatter(formatter)
main_file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(main_file_handler)
    logger.addHandler(console_handler)


def _create_phase_handler(phase_name: str, task_name: str) -> RotatingFileHandler:
    safe_phase = phase_name.replace(" ", "_")
    filename = f"{safe_phase}_{task_name}.log"
    file_path = os.path.join(LOG_DIR, filename)

    handler = RotatingFileHandler(
        file_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler


@contextmanager
def phase_logging(phase_name: str, task_name: str):
    handler = _create_phase_handler(phase_name, task_name)
    logger.addHandler(handler)
    try:
        yield
    finally:
        logger.removeHandler(handler)
        handler.close()
