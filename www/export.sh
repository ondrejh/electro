rsync -av --exclude='*.sh' --exclude='*.txt' ./ pi@192.168.1.220:/home/pi/www/
ssh -t pi@192.168.1.220 "sudo rsync -av /home/pi/www/ /var/www/html/"
