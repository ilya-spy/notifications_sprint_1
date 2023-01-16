import logging

from functools import lru_cache

from core.config import config  # type: ignore

@lru_cache()
def get_logger(name: str):
    """Logger setup"""

    # Create individual module-grained named loggers
    logger: logging.Logger = logging.getLogger(name)
    
    # Create logging handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.setLevel(config.loglevel)

    return logger
