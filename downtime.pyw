import time
from datetime import datetime, timedelta

from config import Config
from log import Log
from schedule import Schedule
from valorant import Valorant
from chrome import Chrome

def main():
    config = Config()

    logger = Log(config.get("output"))
    logger.log("[Main] Script starting...")

    schedule = Schedule(logger, config.get("downtime"))

    apps = []

    if config.get("apps")["valorant"]:
        valorant = Valorant(logger)
        apps.append(valorant)

    if config.get("apps")["chrome"]:
        chrome = Chrome(logger)
        apps.append(chrome)

    try:
        # While the OS is open
        while True:
            schedule.waitUntilNextDowntime()
            logger.log("[Main] These apps will be checked every {} seconds: {}".format(config.get("frequency"), apps))
            deadline = datetime.now() + timedelta(seconds=schedule.timeUntilNextUptime())

            # While we are still in downtime
            while datetime.now() < deadline:
                for app in apps:
                    app.downtime()

                logger.log("[Main] Apps checked.")
                time.sleep(config.get("frequency"))
            
            logger.log("[Main] Downtime has ended.")
    except KeyboardInterrupt:
        logger.log("[Main] Script manually ended.")
    except Exception as e:
        logger.log("[Main] Script unexpectedly ended: {}".format(e))

main()