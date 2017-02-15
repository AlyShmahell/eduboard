<?php

include "./includes/databaseConnect.php";

if (!empty($_SESSION['loggedin']) && !empty($_SESSION['username']))
    include "./public/session.php";
else
    include "./public/login.php";

?>
