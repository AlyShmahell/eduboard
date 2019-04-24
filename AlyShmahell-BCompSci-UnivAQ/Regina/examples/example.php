<?php
require_once __DIR__ . '/../vendor/autoload.php';
use Regina\Regina;
echo Regina::createTable(array("value 1", "value 2"), array(1, 2, 3, 4));
?>