#!/bin/bash

# install pre-requisites
sudo apt install apache2 php phpmyadmin mysql-server mysql-client mysql-workbench

# update apache2 conf file to include phpmyadmin conf file
if grep -qF "Include /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf;then
	sudo bash -c 'echo "Include /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf'
fi
sudo systemctl restart apache2 # now to use phpmyadmin, visit the following url: http://127.0.0.1/phpmyadmin

# install adminer the right way!
sudo mkdir /usr/share/adminer
sudo wget "http://www.adminer.org/latest.php" -O /usr/share/adminer/latest.php
sudo ln -s /usr/share/adminer/latest.php /usr/share/adminer/adminer.php
echo "Alias /adminer.php /usr/share/adminer/adminer.php" | sudo tee /etc/apache2/conf-available/adminer.conf
sudo a2enconf adminer.conf
sudo service apache2 restart # now to use adminer, visit the following url: http://127.0.0.1/adminer.php


