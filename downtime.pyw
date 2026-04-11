import time
from datetime import datetime, timedelta

from log import Log
from schedule import Schedule
from valorant import Valorant
from chrome import Chrome

def main():
    logger = Log()
    logger.log("[Main] Script starting...")

    schedule = Schedule(logger)

    valorant = Valorant(logger)
    chrome = Chrome(logger)

    # While the OS is open
    while True:
        schedule.waitUntilNextDowntime()
        deadline = datetime.now() + timedelta(seconds=schedule.timeUntilNextUptime())

        # While we are still in downtime
        while datetime.now() < deadline:
            logger.log("[Main] Checking apps...")
            valorant.downtime()
            #chrome.downtime()
            time.sleep(30)

main()