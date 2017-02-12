<?php
if (!empty($_POST['username']) && !empty($_POST['password'])) {
    include __DIR__."/../includes/databaseConnect.php";
    include __DIR__."/../includes/functions.php";
    register();
} 
else {
    include __DIR__."/../templates/html/header.html";
    include __DIR__."/../templates/html/register.html";
    include __DIR__."/../templates/html/footer.html";
}
?>

