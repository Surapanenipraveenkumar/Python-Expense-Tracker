import logging
from pathlib import Path

def setup_logger():
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger("expense_tracker")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler("logs/app.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
