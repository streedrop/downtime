import os
import json

class Config():
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

        with open(self.config_file, "r") as file:
            self.config = json.load(file)

    def get(self, key):
        return self.config[key]