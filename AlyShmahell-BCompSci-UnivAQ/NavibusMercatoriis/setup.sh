#!/bin/bash
# install pre-requisites
sudo apt install apache2 php phpmyadmin mysql-server mysql-client mysql-workbench
# install mysql-connector
sudo pip install https://pypi.python.org/packages/2d/28/210962b9b777cd46e454befea235fbaf401ae9b16d704fe9050ddf4e460f/mysql_connector_python-8.0.5-cp27-cp27mu-manylinux1_x86_64.whl#md5=7970fa6a500dd9bcbddd1373d5a77821
# update apache2 conf file to include phpmyadmin conf file
if grep -qF "Include /etc/phpmyadmin/apache.conf" /etc/apache2/apache2.conf;then
	sudo bash -c 'echo "Include /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf'
fi
sudo systemctl restart apache2
