<?php

include "header.php";

if (!empty($_SESSION['loggedin']) && !empty($_SESSION['username']))
    include "session.php";
else
    include "login.php";

?>
