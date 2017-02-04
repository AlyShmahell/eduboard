<?php 
include "databaseConnect.php";
include "functions.php";

include "header.html";
if($_SESSION['usertype']=="user") {
    populate_user_data();
    insert_user_data();
}
    else if($_SESSION['usertype']=="admin") {
        populate_admin_area();
        inspect_user_data();
 } 
include "footer.html";
?>


