import os
import datetime
import time
import subprocess
import sys
import inspect

# Hour where I'm not allowed to play anymore
DOWNTIME_START = 22
DOWNTIME_END = 8
# File that contains in-game logs
VALORANT_LOGFILE = os.path.expandvars("%LOCALAPPDATA%\\VALORANT\\Saved\\Logs\\ShooterGame.log")
VALORANT_LOGFILE_STREAM = None
VALORANT_GAME_STATE = None
# File to outupt script data
OUTPUT_IN_CONSOLE = False
LOGFILE = ".\\downtime.log"

def log(message):
    print("[{}][{}()] {}".format(datetime.datetime.now().strftime("%X"), inspect.currentframe().f_back.f_code.co_name, message))

# Wait until downtime
def timeCheck():
    now = datetime.datetime.now()
    # Past midnight guard (time will be under 10 PM so next checks would return a false positive)
    if(now.hour < DOWNTIME_END):
        log("Time is already late (between midnight and {} AM).".format(DOWNTIME_END))
        return
    
    downtime = datetime.datetime(now.year, now.month, now.day, DOWNTIME_START)
    difference = downtime - now

    if(difference.total_seconds() > 0):
        splitDiff = str(difference).split(':')
        log("Timer started for {} hours, {} minutes and {} seconds.".format(splitDiff[0], splitDiff[1], splitDiff[2].split('.')[0]))
        time.sleep(difference.total_seconds())
        log("Timer has elapsed.")
    else:
        log("Time is already late (between {} PM and midnight).".format(DOWNTIME_START - 12))

    return

# If the specified app is not currently open, returns true
def appCheck(appName):
    if appName in subprocess.run(["tasklist"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout:
        log("{} is open.".format(appName))
        return True
    
    log("{} is not open.".format(appName))
    return False

def appKill(appName):
    log("Exiting {}. Downtime has passed.".format(appName))
    subprocess.run(["taskkill", "/F", "/IM", appName], creationflags=subprocess.CREATE_NO_WINDOW)

# Check the state of VALORANT, keep looping while I am still in game
def inGameCheck():
    global VALORANT_LOGFILE_STREAM

    # Open log file if needed
    if VALORANT_LOGFILE_STREAM is None:
        VALORANT_LOGFILE_STREAM = open(VALORANT_LOGFILE)

    # Retrieve game state and log it
    updateCurrentGameState()
    log("Current game state: {}.".format(VALORANT_GAME_STATE))

    # If not in game, close file and return false
    if(VALORANT_GAME_STATE == "Menu"):
        VALORANT_LOGFILE_STREAM.close()
        VALORANT_LOGFILE_STREAM = None
        return False
    
    # If in game, return true
    return True

# Return the current game state, "Menu" or "Playing"
def updateCurrentGameState():
    global VALORANT_GAME_STATE

    # Read remaining lines from logfile and
    for line in VALORANT_LOGFILE_STREAM:
        if "LogGameFlowStateManager" in line:
            if("Transitioning from Pregame to TransitionToInGame" in line
                or "Current state TransitionToInGame" in line 
                or "Current state InGame" in line
            ):
                VALORANT_GAME_STATE = "Playing"

            if("Transitioning from InGame to TransitionToMainMenu" in line
                or "Current state TransitionToMainMenu" in line 
                or "Current state MainMenu" in line
            ):
                VALORANT_GAME_STATE = "Menu"

    # If no games were started yet
    if VALORANT_GAME_STATE is None:
        VALORANT_GAME_STATE = "Menu"

def valoCheck():
    if(appCheck("VALORANT")):
        if(inGameCheck() is False):
            appKill("VALORANT-Win64-Shipping.exe")

def chromeCheck():
    if(appCheck("chrome")):
        appKill("chrome.exe")

def main():
    # Log data in the log file
    if not OUTPUT_IN_CONSOLE:
        logfile = open(LOGFILE, "w", buffering=1)
        sys.stdout = logfile

    log("Script starting...")
    timeCheck()

    # While the OS is open
    while True:
        log("Checking apps...")
        valoCheck()
        chromeCheck()
        time.sleep(60)

main()