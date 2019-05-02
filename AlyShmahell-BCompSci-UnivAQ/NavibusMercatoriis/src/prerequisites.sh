#!/bin/bash

sudo apt install apache2 php phpmyadmin mysql-server mysql-client mysql-workbench

sudo service mysql start

if grep -qF "Include /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf; then
	sudo bash -c 'echo "Include /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf'
fi
sudo systemctl restart apache2

sudo mkdir /usr/share/adminer
sudo wget "http://www.adminer.org/latest.php" -O /usr/share/adminer/latest.php
sudo ln -s /usr/share/adminer/latest.php /usr/share/adminer/adminer.php
echo "Alias /adminer.php /usr/share/adminer/adminer.php" | sudo tee /etc/apache2/conf-available/adminer.conf
sudo a2enconf adminer.conf
sudo service apache2 restart

sudo mysql -u root -p$@ -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$@';"

