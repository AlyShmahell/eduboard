<?php 
session_start();

include __DIR__."/../includes/databaseConnect.php";
include __DIR__."/../includes/functions.php";

if (!empty($_SESSION['username']) && !empty($_SESSION['loggedin'])) 
{
    ob_start();
    include __DIR__."/../templates/html/header.html";
    if($_SESSION['usertype']=="usertype1"||$_SESSION['usertype']=="usertype2") 
    {
        populate_user_data();
        insert_user_data();
    }
    else if($_SESSION['usertype']=="admin") 
    {
        populate_admin_area();
        inspect_user_data();
        change_group_permissions();
        change_user_group();
    } 
    include __DIR__."/../templates/html/footer.html";  
}
else
{
    header("Location: http://localhost/");
}


?>


