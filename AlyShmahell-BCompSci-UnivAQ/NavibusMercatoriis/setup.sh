#!/bin/bash
# install pre-requisites
sudo apt install apache2 php phpmyadmin mysql-server mysql-client mysql-workbench
# update apache2 conf file to include phpmyadmin conf file
if grep -qF "Include /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf;then
	sudo bash -c 'echo "Include /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf'
fi
sudo systemctl restart apache2
