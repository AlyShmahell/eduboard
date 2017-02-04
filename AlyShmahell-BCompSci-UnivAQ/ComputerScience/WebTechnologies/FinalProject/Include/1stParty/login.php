<?php
if (!empty($_POST['username']) && !empty($_POST['password'])) {
    include "databaseConnect.php";
    include "functions.php";
    login();
}
else
{
    include "header.html";
    include "login.html";
    include "footer.html";
}
?>

