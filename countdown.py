import time


class Countdown():
    def __init__(self, secs):
        self.secs = secs

    def startCountdown(self):
        while self.secs:
            #mins, secs = divmod(self.secs, 60)
            #self.draw(win, timeformat)
            time.sleep(1)
            self.secs -= 1
        print('end countdown')

    def getTime(self):
        return self.secs
