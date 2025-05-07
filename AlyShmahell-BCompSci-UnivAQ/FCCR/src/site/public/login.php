<?php
session_start();
if (!empty($_POST['username']) && !empty($_POST['password'])) {
    include __DIR__."/../includes/mysqli.php";
    include __DIR__."/../includes/functions.php";
    login($connection);
}
else
{
    include __DIR__."/../templates/html/header.html";
    include __DIR__."/../templates/html/login.html";
    include __DIR__."/../templates/html/footer.html";
}
?>

