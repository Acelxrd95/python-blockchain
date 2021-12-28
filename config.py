# add a logger for config file
from logging import getLogger, StreamHandler, Formatter, INFO

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.setLevel(INFO)
logger.addHandler(handler)
