import datetime
import inspect

import logging

class Log():
    def __init__(self):
        self.output_in_console = True
        self.output_in_file = True

        self.logger = logging.getLogger("downtime")
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter("[%(asctime)s]%(message)s", datefmt="%X")

        # Console handler
        if self.output_in_console:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)

        # File handler
        if self.output_in_file:
            self.file_handler = logging.FileHandler("downtime.log", mode="w")
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)

    def log(self, message):
        self.logger.info(message)
        #print("[{}][{}()] {}".format(datetime.datetime.now().strftime("%X"), inspect.currentframe().f_back.f_code.co_name, message))
