<?php

$host = "localhost";
$mysqlUser = "root";
$mysqlPassword = "toor";
$database = "webtech";

$connection = mysql_connect($host, $mysqlUser, $mysqlPassword) or die("mySQL Error: " . mysql_error());
$databaseSelect = mysql_select_db($database) or die ("mySQL Error: " . mysql_error());
?>
