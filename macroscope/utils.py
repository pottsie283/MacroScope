import logging
import os

def setup_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def safe_extract_path(base_dir: str, filename: str) -> str:
    # Prevent path traversal
    safe_name = os.path.basename(filename)
    return os.path.join(base_dir, safe_name)
