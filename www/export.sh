scp * pi@192.168.1.220:/home/pi/www/
ssh -t pi@192.168.1.220 "sudo cp /home/pi/www/* /var/www/html/"
