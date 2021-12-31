from logging import getLogger, StreamHandler, Formatter, INFO, DEBUG


def set_logger(level=INFO):
    """
    Set logger.
    """
    handler.setLevel(level)
    handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.info("Logger set.")


logger = getLogger(__name__)
handler = StreamHandler()
set_logger(DEBUG)
