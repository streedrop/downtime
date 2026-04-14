import os

import logging

class Log():
    def __init__(self, config):
        self.output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downtime.log")

        self.logger = logging.getLogger("downtime")
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter("[%(asctime)s]%(message)s", datefmt="%X")

        # Console handler
        if config["console"]:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)

        # File handler
        if config["file"]:
            self.file_handler = logging.FileHandler(self.output_file, mode="w")
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

    def log(self, message):
        self.logger.info(message)
        #print("[{}][{}()] {}".format(datetime.datetime.now().strftime("%X"), inspect.currentframe().f_back.f_code.co_name, message))
