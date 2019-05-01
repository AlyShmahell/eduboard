<?php
include __DIR__."/includes/mysqli.php";

if (!empty($_SESSION['loggedin']) && !empty($_SESSION['username']))
    include __DIR__."/public/session.php";
else
    include __DIR__."/public/login.php";

?>
