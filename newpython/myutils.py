#!/usr/bin/python3

from subprocess import Popen, PIPE
import RPi.GPIO as GPIO

LCD_LIGHT_OUTPUT = 18
BUTTON_1_INPUT = 5
BUTTON_2_INPUT = 6
BUTTON_3_INPUT = 13


def get_my_ip():
    cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    p = Popen(cmd, shell=True, stdout=PIPE)
    myip = p.communicate()[0]
    return myip.decode('ascii').strip()


def get_onoff(prompt):
    while True:
        try:
            return {"on": True, "off": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter ON or OFF")


class my_gpios(object):
    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(LCD_LIGHT_OUTPUT, GPIO.OUT)
        GPIO.setup([BUTTON_1_INPUT, BUTTON_2_INPUT, BUTTON_3_INPUT], GPIO.IN)

    def lcd_light(self, status=True):

        GPIO.output(LCD_LIGHT_OUTPUT, 1 if status else 0)

    def get_buttons(self, btn=None):

        if btn == 1:
            return False if GPIO.input(BUTTON_1_INPUT) else True
        if btn == 2:
            return False if GPIO.input(BUTTON_2_INPUT) else True
        if btn == 3:
            return False if GPIO.input(BUTTON_3_INPUT) else True

        btn1 = False if GPIO.input(BUTTON_1_INPUT) else True
        btn2 = False if GPIO.input(BUTTON_2_INPUT) else True
        btn3 = False if GPIO.input(BUTTON_3_INPUT) else True

        return (btn1, btn2, btn3)


if __name__ == "__main__":

    gpios = my_gpios()

    myip = get_my_ip()
    print(myip)

    gpios.lcd_light(get_onoff("LCD backlight status: "))

    from time import sleep

    for i in range(10):
        sleep(1)
        btns = gpios.get_buttons()
        print(btns)
