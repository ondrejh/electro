#!/usr/bin/python3

import datetime

from lcd1602 import Adafruit_CharLCD as Lcd1602
from myutils import MyGpios, Button, get_my_ip, center_text


def ip_page():

    ip = get_my_ip()
    ip = center_text(ip)

    return " My IP address: \n" + ip


def clock_page():

    d = datetime.datetime.now()

    return center_text(d.strftime("%a %d.%m.%Y")) + "\n" + center_text(d.strftime("%H:%M:%S"))


def empty_page():

    return "   Empty Page   \n  Hello world!  "


class Page(object):

    def __init__(self, refresh, period=None):

        self.refresh = refresh
        self.period = period
        self.content = self.refresh()
        self.refreshed = datetime.datetime.now()

    def refresh_anyway(self):

        self.content = self.refresh()
        self.refreshed = datetime.datetime.now()

    def refresh_if_needed(self):

        if self.period is None:
            return False

        if (datetime.datetime.now() - self.refreshed).seconds > self.period:
            self.refresh_anyway()
            return True

        return False


pages = (Page(clock_page, period=0.2),
         Page(ip_page, period=120),
         Page(empty_page, period=None))

LIGHT_ON_TIME = 10.0  # seconds


if __name__ == "__main__":

    lcd = Lcd1602()
    ios = MyGpios()

    page_cnt = 0
    pages[page_cnt].refresh_if_needed()
    lcd.message(pages[page_cnt].content)
    light_on = True
    light_time = datetime.datetime.now()

    button_set = Button(lambda x=1: ios.get_buttons(x))
    button_left = Button(lambda x=2: ios.get_buttons(x))
    button_right = Button(lambda x=3: ios.get_buttons(x))

    while True:
        button_set.read()
        button_left.read()
        button_right.read()

        if button_right.pressed:
            page_cnt += 1
        elif button_left.pressed:
            page_cnt -= 1
        elif button_set.pressed:
            if not light_on:
                light_time = datetime.datetime.now()
                ios.lcd_light(True)
                light_on = True
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
