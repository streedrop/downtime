from datetime import datetime, timedelta
import time

from enum import Enum

class Week(Enum):
    SUNDAY = 6
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5

class Schedule():
    def __init__(self, logger):
        self.logger = logger

        """
        self.uptime = {
            Week.SUNDAY.value: [[8, 22]],
            Week.MONDAY.value: [[8, 22]],
            Week.TUESDAY.value: [[8, 22]],
            Week.WEDNESDAY.value: [[8, 22]],
            Week.THURSDAY.value: [[8, 22]],
            Week.FRIDAY.value: [[8, 24]],
            Week.SATURDAY.value: [[8, 24]]
        }
        """

        self.downtime = {
            Week.SUNDAY.value: [[0, 8], [22, 24]],
            Week.MONDAY.value: [[0, 8], [22, 24]],
            Week.TUESDAY.value: [[0, 8], [22, 24]],
            Week.WEDNESDAY.value: [[0, 8], [22, 24]],
            Week.THURSDAY.value: [[0, 8], [22, 24]],
            Week.FRIDAY.value: [[0, 8]],
            Week.SATURDAY.value: [[0, 8]]
        }

    
    def inDowntime(self):
        now = datetime.now()

        for period in self.downtime[now.weekday()]:
            if now.hour >= period[0] and now.hour < period[1]:
                return True
            
        return False
    
    def timeUntilNextDowntime(self):
        if self.inDowntime(): return 0

        now = datetime.now()
        downtime = None

        # Check the entire next week
        for i in range(7):
            # Check every downtime in the week
            for period in self.downtime[(now.weekday() + i) % 7]:
                # If it's another day or a downtime that hasn't happened yet today:
                if i > 0 or now.hour < period[0]:
                    date = now + timedelta(days=i)
                    downtime = datetime(date.year, date.month, date.day, period[0])
                    break
            if downtime is not None:
                break

        if downtime is None:
            raise ValueError("No next downtime")

        difference = downtime - now

        if difference.total_seconds() > 0:
            splitDiff = str(difference).split(':')
            self.logger.log("[Schedule] Next downtime in {} hours, {} minutes and {} seconds.".format(splitDiff[0], splitDiff[1], splitDiff[2].split('.')[0]))

        return difference.total_seconds()
    
    def timeUntilNextUptime(self):
        if not self.inDowntime(): return 0

        now = datetime.now()
        uptime = None
        # Check the entire next week
        for i in range(7):
            # Check every downtime in the day
            for period in self.downtime[(now.weekday() + i) % 7]:
                # If it's another day or an uptime that hasn't happened yet today:
                if i > 0 or now.hour < period[1]:
                    date = now + timedelta(days=i)
                    uptime = datetime(date.year, date.month, date.day, period[1] % 24)

                    # Check every next day of the week, starting tomorrow
                    for j in range(1, 9):
                        # If the hours isn't 24, we're ok, quit for loop
                        if uptime.hour != 0:
                            break
                        # If the whole week has been done, there's no uptime remaining
                        if j == 8:
                            raise ValueError("No next uptime")
                        # If it continues tomorrow, find the end of tomorrow's downtime and loop back to make sure it's not 24
                        if self.downtime[(date.weekday() + j) % 7][0][0] == 0:
                            next_date = date + timedelta(days=j)
                            uptime = datetime(next_date.year, next_date.month, next_date.day, self.downtime[(next_date.weekday() + j) % 7][0][1] % 24)
                        # It doesn't continue tomorrow, we're good
                        else:
                            break
                    break
            if uptime is not None:
                break

        difference = uptime - now

        if difference.total_seconds() > 0:
            splitDiff = str(difference).split(':')
            self.logger.log("[Schedule] Next uptime in {} hours, {} minutes and {} seconds.".format(splitDiff[0], splitDiff[1], splitDiff[2].split('.')[0]))

        return difference.total_seconds()

    def waitUntilNextDowntime(self):
        difference = self.timeUntilNextDowntime()

        if difference > 0:
            time.sleep(difference)

        self.logger.log("[Schedule] In downtime.")

    def waitUntilNextUptime(self):
        difference = self.timeUntilNextUptime()

        if difference > 0:
            time.sleep(difference)

        self.logger.log("[Schedule] In uptime.")