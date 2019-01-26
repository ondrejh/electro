from Adafruit_CharLCD import Adafruit_CharLCD
from myutils import my_gpios, get_my_ip
from time import sleep
import datetime


def ip_page():

    ip = get_my_ip()
    af = (16 - len(ip)) // 2
    bf = 16 - len(ip) - af
    ip = (' ' * bf) + ip + (' ' * af)

    return " My IP address: \n" + ip
    #return " My IP address: \n 192.168.1.220  "


def clock_page():

    return "     Clock      \n    12:34:56    "


def empty_page():

    return "   Empty Page   \n  Hello world!  "


class Page(object):

    def __init__(self, refresh, period=1.0):

        self.refresh = refresh
        self.period = period
        self.content = self.refresh()
        self.refreshed = datetime.datetime.now()

    def refresh_anyway(self):

        self.content = self.refresh()
        self.refreshed = datetime.datetime.now()

    def refresh_if_needed(self):

        if (datetime.datetime.now() - self.refreshed).seconds > self.period:
            self.refresh_anyway()
            return True
        else:
            return False


pages = (Page(empty_page, period=120),
         Page(clock_page, period=0.2),
         Page(ip_page, period=10))

LIGHT_ON_TIME = 10.0  # seconds


if __name__ == "__main__":

    lcd = Adafruit_CharLCD()
    ios = my_gpios()

    page_cnt = 0
    pages[page_cnt].refresh_if_needed()
    lcd.message(pages[page_cnt].content)
    light_on = True
    light_time = datetime.datetime.now()

    while True:
        buttons = ios.get_buttons()

        if buttons[2]:
            page_cnt += 1
        elif buttons[1]:
            page_cnt -= 1
        elif buttons[0]:
            if not light_on:
                light_time = datetime.datetime.now()
                ios.lcd_light(True)
                light_on = True
            pass
        else:
            if light_on:
                if (datetime.datetime.now() - light_time).seconds >= LIGHT_ON_TIME:
                    light_on = False
                    ios.lcd_light(False)
            if not pages[page_cnt].refresh_if_needed():
                lcd.setCursor(0, 0)
                lcd.message(pages[page_cnt].content)
            continue

        light_time = datetime.datetime.now()
        ios.lcd_light(True)
        light_on = True

        page_cnt %= len(pages)
        if pages[page_cnt].refresh_if_needed():
            lcd.setCursor(0, 0)
            lcd.message(pages[page_cnt].content)
