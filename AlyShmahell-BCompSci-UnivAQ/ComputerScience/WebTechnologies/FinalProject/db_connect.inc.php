<?php

session_start();

define("host","localhost");
define("user","root");
define("password","toor");
define("database","webtech");

$conn = mysql_connect(host,user,password) or die("mySQL Error: " . mysql_error());
$db = mysql_select_db(database) or die ("mySQL Error: " . mysql_error());
?>
