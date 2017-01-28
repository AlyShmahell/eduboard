#!/bin/bash

echo mysql -u root -p create database webtech;
echo "create database webtech" | mysql -u root -p 
echo mysql -u root -p webtech < users.sql
mysql -u root -p webtech < users.sql
echo mysql -u root -p webtech < shares.sql 
mysql -u root -p webtech < shares.sql 
