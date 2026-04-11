import os

from app import App

class Chrome():
    def __init__(self, logger):
        self.app = App(logger, "Chrome", "chrome.exe")
    
    def downtime(self):
        if self.app.isOpen():
            self.app.close()