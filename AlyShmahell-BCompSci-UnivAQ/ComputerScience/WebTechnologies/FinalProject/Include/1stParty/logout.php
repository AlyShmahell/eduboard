<?php 
include "header.php";
$_SESSION = array();
session_destroy();
header("Location: http://localhost/public");
?>
