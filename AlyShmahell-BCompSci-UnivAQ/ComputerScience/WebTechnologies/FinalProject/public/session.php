<?php 
include __DIR__."/../includes/databaseConnect.php";
include __DIR__."/../includes/functions.php";

include __DIR__."/../templates/html/header.html";
if($_SESSION['usertype']=="user") {
    populate_user_data();
    insert_user_data();
}
    else if($_SESSION['usertype']=="admin") {
        populate_admin_area();
        inspect_user_data();
 } 
include __DIR__."/../templates/html/footer.html";
?>


