<?php

$host          = "";
$username      = "";
$password      = "";
$database      = "";
$port          = 1;

$lines = file(__DIR__ . '/mysql_credentials.txt');
$credentials = array();

foreach($lines as $line) {
    if(empty($line)) continue;

    $line = trim(str_replace(": ", ':', $line));
    $line_array = explode(' ', $line);

    // host
    $host = explode(':', $line_array[0]);
    $host = array_pop($host);

    // username
    $username = explode(':', $line_array[1]);
    $username = array_pop($username);

    // password
    $password = explode(':', $line_array[2]);
    $password = array_pop($password);

    // database
    $database = explode(':', $line_array[3]);
    $database = array_pop($database);

    // database
    $port = explode(':', $line_array[4]);
    $port = array_pop($port);
}

$connection     = new mysqli($host, $username, $password, $database);

?>
