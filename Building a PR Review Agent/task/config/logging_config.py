import logging


# Setup logging
def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    # Get logger
    logger = logging.getLogger(name)

    # set the level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # clear existing handlers
    logger.handlers.clear()

    # Create handler
    handler = logging.StreamHandler()
    handler.setLevel(log_level)

    # set up the formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Attach handler
    logger.addHandler(handler)

    return logger
