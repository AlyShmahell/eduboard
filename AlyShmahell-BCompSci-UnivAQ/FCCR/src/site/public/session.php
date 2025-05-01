<?php 
session_start();

include __DIR__."/../includes/mysqli.php";
include __DIR__."/../includes/functions.php";

if (!empty($_SESSION['username']) && !empty($_SESSION['loggedin'])) 
{
    ob_start();
    include __DIR__."/../templates/html/header.html";
    if(strpos( $_SESSION['usertype'], "user") !== false) 
    {
        populate_user_data($connection);
        insert_user_data($connection);
    }
    else if($_SESSION['usertype']=="admin") 
    {
        populate_admin_area($connection);
        inspect_user_data($connection);
        change_group_permissions($connection);
        change_user_group($connection);
    } 
    include __DIR__."/../templates/html/footer.html";  
}
else
{
    header("Location: http://localhost:".$_SERVER['SERVER_PORT']."/");
}


?>


