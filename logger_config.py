
import logging

from keys import Keys

class LoggerConfig:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dir_log = Keys.get_arq_log()
        if not self.logger.hasHandlers():
            handler = logging.FileHandler(self.dir_log)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.logger
