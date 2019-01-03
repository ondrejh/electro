#!/usr/bin/python3

from subprocess import Popen, PIPE
import RPi.GPIO as GPIO

LCD_LIGHT_OUTPUT = 18

def get_my_ip():

	cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
	p = Popen(cmd, shell=True, stdout=PIPE)
	myip = p.communicate()[0]
	return myip.decode('ascii').strip()


def lcd_light(status=True, init=False):

	if init:
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(LCD_LIGHT_OUTPUT, GPIO.OUT)

	GPIO.output(LCD_LIGHT_OUTPUT, 1 if status else 0)


def get_onoff(prompt):
	while True:
		try:
			return {"on":True, "off":False}[input(prompt).lower()]
		except KeyError:
			print("Invalid input please enter ON or OFF")


if __name__ == "__main__":

	myip = get_my_ip()
	print(myip)

	lcd_light(get_onoff("LCD backlight status: "), True)
