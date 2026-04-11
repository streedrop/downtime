import subprocess

class App():
    def __init__(self, logger, name, process_name, taskkill_name = None):
        self.logger = logger
        self.name = name
        self.process_name = process_name
        self.taskkill_name = taskkill_name
    
    def isOpen(self):
        if self.process_name in subprocess.run(["tasklist"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout:
            self.logger.log("[{}] {} is open.".format(self.name, self.name))
            return True
        
        self.logger.log("[{}] {} is not open.".format(self.name, self.name))
        return False

    def close(self):
        self.logger.log("[{}] Exiting {}. Downtime has passed.".format(self.name, self.name))

        if self.taskkill_name is None:
            subprocess.run(["taskkill", "/F", "/IM", self.process_name], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.run(["taskkill", "/F", "/IM", self.taskkill_name], creationflags=subprocess.CREATE_NO_WINDOW)