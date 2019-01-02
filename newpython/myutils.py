#!/usr/bin/python3

from subprocess import Popen, PIPE

def get_my_ip():

	cmd = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
	p = Popen(cmd, shell=True, stdout=PIPE)
	myip = p.communicate()[0]
	return myip.decode('ascii').strip()

if __name__ == "__main__":

	myip = get_my_ip()
	print(myip)
