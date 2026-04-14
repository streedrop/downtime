from app import App

class Chrome(App):
    def __init__(self, logger):
        super().__init__(logger, "Chrome", "chrome.exe")
    
    def downtime(self):
        if self.isOpen():
            self.close()