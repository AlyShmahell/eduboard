# FCCR : Federal Corporate Claim Registry

a PHP7 website that simulates a claim registry where companies (users) can register their asset claims and officials (admins) can inspect these assets.  

### OS Support
- Ubuntu 18.04

### Usage:
#### Requirements
```sh
sudo apt update  
sudo apt install mysql-server php php-mysqli php-mysql python3.6  
```
#### Configuration
```sh
./setup -host <address> -port <port_number> -u <mysql_user> -p <mysql_password> -db fccr
```
#### Running
```sh
./create_admin -u <mysql_user> -db fccr -admin <admin_name> -password <admin_password>  
./run
```