<?php
include("Regina/Regina.inc.php");

if (!function_exists('credit')) 
{
    function credit() 
    {
        $_SESSION['username'] = mysql_real_escape_string($_POST['username']);
        $_SESSION['username'] = preg_replace('/\s+/', '', $_SESSION['username']);
        $_SESSION['password'] = mysql_real_escape_string($_POST['password']);
        $_SESSION['password'] = preg_replace('/\s+/', '', $_SESSION['password']);
        $_SESSION['user_table'] = hash('sha1', $_SESSION['username'] . $_SESSION['password']);
        $_SESSION['user_table'] = "a" . $_SESSION['user_table'];
        $_SESSION['password'] = hash('sha512', $_SESSION['password']);
    }
}

if(!function_exists('notify')) 
{
    function notify($notifyTitle,$notifyMessage) 
    {
        $html = file_get_contents(__DIR__."/../templates/html/header.html");
        $html = $html . file_get_contents(__DIR__."/../templates/html/failure.html");
        $html = $html . file_get_contents(__DIR__."/../templates/html/footer.html");
        $html  = str_replace("{{title}}",$notifyTitle,$html);
        $html  = str_replace("{{message}}",$notifyMessage,$html);
        echo $html;
        $_SESSION = array();
        session_destroy();
    }
}


if (!function_exists('login')) 
{
    function login()
    {
        credit();
        $checkLoginInUsers = mysql_query("SELECT * FROM users WHERE username='" . $_SESSION['username'] . "' AND pass_word = '" . $_SESSION['password'] . "'");
        $checkLoginInAdmins = mysql_query("SELECT * FROM admins WHERE username='" . $_SESSION['username'] . "' AND pass_word = '" . $_SESSION['password'] . "'");
        if (mysql_num_rows($checkLoginInUsers) == 1) 
        {
            $row = mysql_fetch_array($checkLoginInUsers);
            $_SESSION['loggedin'] = 1;
            $_SESSION['usertype'] = "user";
            header("Location: http://localhost/public/session.php");
        } 
        else if (mysql_num_rows($checkLoginInAdmins) == 1) 
        {
            $row = mysql_fetch_array($checkLoginInAdmins);
            $_SESSION['loggedin'] = 1;
            $_SESSION['usertype'] = "admin";
            $admin_db = mysql_query("CREATE TABLE ".$_SESSION['username']."(corporation VARCHAR(767) UNIQUE PRIMARY KEY, database_token VARCHAR(767))");
            header("Location: http://localhost/public/session.php");
        } 
        else
            notify("Error","Wrong Credentials");  
    }
}

if (!function_exists('register')) 
{
    function register()
    {
        credit();
        $checkusername = mysql_query("SELECT * FROM groups WHERE username='" . $_SESSION['username'] . "'");
        if (mysql_num_rows($checkusername) == 1) 
        {
            $checkusernameInAdmins = mysql_query("SELECT * FROM admins WHERE username='" . $_SESSION['username'] . "'");
            $checkusernameInUsers = mysql_query("SELECT * FROM users WHERE username='" . $_SESSION['username'] . "'");
            if (mysql_num_rows($checkusernameInAdmins) == 1 || mysql_num_rows($checkusernameInUsers) == 1) 
            {
                notify("Error","Credentials already in use!");
                header("Refresh:10");
            } 
            else 
            {
                $registerquery = mysql_query("INSERT INTO users (username,pass_word) VALUES('" . $_SESSION['username'] . "','" . $_SESSION['password'] . "')");
                if ($registerquery) 
                {
                    mysql_query("CREATE TABLE ". $_SESSION['user_table'] ."(assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE)");
                    notify("Success","Your account was successfully created. You're being redirected to the login page");
                    header("Refresh:10");
                } 
                else 
                    notify("Error","Sorry, your registration failed. Please go back and try again1.");
            }
        } 
        else 
        {
            mysql_query("INSERT INTO groups (username) VALUES('" . $_SESSION['username'] . "')");
            $registerquery = mysql_query("INSERT INTO users (username,pass_word) VALUES('" . $_SESSION['username'] . "','" . $_SESSION['password'] . "')");
            if ($registerquery)
            {
                mysql_query("CREATE TABLE webtech.". $_SESSION['user_table'] ."(assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE)");
                notify("Success","Your account was successfully created. You're being redirected to the login page");
                header("Refresh:10");
            } 
            else
                notify("Error","Sorry, your registration failed. Please go back and try again2.");
        }
    }
}

if (!function_exists('populate_user_data')) 
{
    function populate_user_data()
    {
        /** Presentation Logic: populate_user_data **/
        $html = file_get_contents(__DIR__."/../templates/html/session_regularUserArea.html");
        $html = str_replace("{{regularUser}}", $_SESSION['username'], $html);
        $user_data = array();
        $user_data = mysql_query("SELECT * FROM ".$_SESSION['user_table']);
        if (!mysql_num_rows($user_data))
            $html = str_replace("{{regularUserAssetsTable}}","You have no assets yet!", $html);
        else 
        { 
            $table = array();
            for($i = 0; $i < mysql_num_rows($user_data);  $i++)
            {
                $user_data_row =  mysql_fetch_array($user_data);
                array_push($table,$user_data_row[0]);
                array_push($table,$user_data_row[1]);
            }
            $html = str_replace("{{regularUserAssetsTable}}", createTable(array("Asset Name", "Asset Location"),$table), $html); 
        }



        /** Hybrid Logic: Respond to Inspection **/
        $inspection_admins = mysql_query("SELECT * FROM admins");
        if (!mysql_num_rows($inspection_admins))
            $html = str_replace("{{inspectionRequest}}","No Admins! Oh it's chaos :D",$html);
        else while ($inspection_admins_onebyone = mysql_fetch_array($inspection_admins)) 
        {
            $inspection_requests = mysql_query("SELECT * FROM ".$inspection_admins_onebyone[0]." WHERE corporation = '" . $_SESSION['username'] . "'");
            if (!mysql_num_rows($inspection_requests))
                $html = str_replace("{{inspectionRequest}}","No inspections! Oh joy! *_*",$html);
            else while ($respond_to_request = mysql_fetch_array($inspection_requests)) 
            {
                if ($respond_to_request[1] == '0')
                {
                    $inspection_granted = mysql_query("UPDATE " . $inspection_admins_onebyone[0] . " SET database_token = '" . $_SESSION['user_table'] . "' WHERE corporation = '" . $_SESSION['username'] . "'");
                    if ($inspection_granted)
                        $html = str_replace("{{inspectionRequest}}","admin '" . $inspection_admins_onebyone[0] . "' was granted inspection rights",$html);
                }
            }
        }
        $html = str_replace("{{inspectionRequest}}","No New Inspection Requests",$html);
        echo $html;
    }
}

if (!function_exists('insert_user_data'))
{
    function insert_user_data()
    {
        /** Business Logic: insert_user_data **/
        if (!empty($_POST['assetname']) && !empty($_POST['assetcoordinates'])) 
        {
            $user_data_inserted = mysql_query("INSERT INTO ".$_SESSION['user_table']."(assetname,assetcoordinates) VALUES('" . $_POST['assetname'] . "', '" . $_POST['assetcoordinates'] . "')");
            if ($user_data_inserted == 1)
                header("Refresh:0");
        }
    }
}


if (!function_exists('populate_admin_area')) 
{
    function populate_admin_area()
    {
        $html = file_get_contents(__DIR__."/../templates/html/session_adminUserArea.html");
        $html = str_replace("{{adminUser}}", $_SESSION['username'], $html);
        $admin_data = mysql_query("SELECT * FROM groups");
        if (!mysql_num_rows($admin_data))
            $html = str_replace("{{regularUsersTable}}", "Unfortunately there seems to be no corporations on record, peace failed and the world was destroyed :)", $html);
        else
        {

            $table = array();
            for($i = 0; $i < mysql_num_rows($admin_data);  $i++)
            {
                $user_data_array =  mysql_fetch_array($admin_data);
                if ($user_data_array[1] == "user")
                    array_push($table,$user_data_array[0]);
            }
            $html = str_replace("{{regularUsersTable}}", createTable(array("Corporation Name"),$table), $html); 

        }


        $inspection_rights = mysql_query("SELECT * FROM " . $_SESSION['username']);
        if (!mysql_num_rows($inspection_rights))
            $html = str_replace("{{inspectionTable}}", "No inspection rights granted yet", $html);
        else while ($inspection_rights_array = mysql_fetch_array($inspection_rights)) 
        {
            $html = str_replace("{{inspectionTable}}",$inspection_rights_array[0].", {{inspectionTable}}", $html);
            $inspection_granted_data = mysql_query("SELECT * FROM " . $inspection_rights_array[1]);
            if (mysql_num_rows($inspection_granted_data))
            {
                $table = array();
                for($i = 0; $i < mysql_num_rows($inspection_granted_data);  $i++)
                {
                    $inspection_granted_data_array = mysql_fetch_array($inspection_granted_data);
                    array_push($table,$inspection_granted_data_array[0]);
                    array_push($table,$inspection_granted_data_array[1]);
                }
                $html = str_replace(", {{inspectionTable}}", createTable(array("Asset Name","Asset Location"),$table)."{{inspectionTable}}", $html);
                mysql_query("DELETE FROM " . $_SESSION['username'] . " WHERE database_token != '0'");
            }
        }
        $html = str_replace(", {{inspectionTable}}", "", $html);
        echo $html;
    }
}

if (!function_exists('inspect_user_data')) 
{
    function inspect_user_data()
    {
        if(!empty($_POST['usertoinspect'])&&isset($_POST['usertoinspect']))
        {
            $username = $_SESSION['username'];
            $usertoinspect = $_POST['usertoinspect'];
            $usertoinspect = mysql_real_escape_string($usertoinspect);
            $usertoinspect = preg_replace('/\s+/', '', $usertoinspect);
            if (!empty($username) && !empty($usertoinspect)) 
            {
                $inspection_requested = mysql_query("INSERT INTO webtech.$username (corporation,database_token) VALUES('$usertoinspect','0')");

            }
            header("Refresh:0");
        }
    }
}

?>
