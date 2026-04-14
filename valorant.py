import os

from app import App

class Valorant(App):
    def __init__(self, logger):
        super().__init__(logger, "Valorant", "VALORANT-Win64-Shipping", "VALORANT-Win64-Shipping.exe")
        # File that contains in-game logs
        self.logfile_name = os.path.expandvars("%LOCALAPPDATA%\\VALORANT\\Saved\\Logs\\ShooterGame.log")
        self.logfile = open(self.logfile_name)
        # Current game state
        self.in_game = False
    
    def downtime(self):
        if self.isOpen():
            if not self.isInGame():
                self.close()
            else:
                self.logger.log("[Valorant] Still in game. Not closing.")

    # Returns whether I am in game or not with proper file management
    def isInGame(self):

        if self.logfile is None:
            self.logfile = open(self.logfile_name)

        # Retrieve game state and log it
        self.updateGameState()
        self.logger.log("[Valorant] InGame: {}".format(self.in_game))

        # If not in game, close file and return false
        if not self.in_game:
            self.logfile.close()
            self.logfile = None
        
        # If in game, return true and keep file open
        return self.in_game
    
    # Updates the current game state by reading the log file
    def updateGameState(self):
        # Read remaining lines from logfile
        for line in self.logfile:
            if "LogGameFlowStateManager" in line:
                if("Transitioning from Pregame to TransitionToInGame" in line
                    or "Current state TransitionToInGame" in line 
                    or "Current state InGame" in line
                ):
                    self.in_game = True

                if("Transitioning from InGame to TransitionToMainMenu" in line
                    or "Current state TransitionToMainMenu" in line 
                    or "Current state MainMenu" in line
                ):
                    self.in_game = False