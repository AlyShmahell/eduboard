<?php 
include __DIR__."/../includes/mysqli.php";
session_start();
$_SESSION = array();
session_destroy();
header("Location: http://localhost:".$_SERVER['SERVER_PORT']."/");
?>
