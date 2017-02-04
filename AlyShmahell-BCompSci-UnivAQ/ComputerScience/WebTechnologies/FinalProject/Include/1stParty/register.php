<?php
if (!empty($_POST['username']) && !empty($_POST['password'])) {
    include "databaseConnect.php";
    include "functions.php";
    register();
} 
else {
    include "header.html";
    include "register.html";
    include "footer.html";
}
?>

