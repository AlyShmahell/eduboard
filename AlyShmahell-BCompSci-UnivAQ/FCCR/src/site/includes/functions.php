<?php
require_once("Regina/Regina.php");
use Regina\Regina;


if (!function_exists('credit')) 
{
    function credit($connection) 
    {
        $_SESSION['username'] = mysqli_real_escape_string($connection, $_POST['username']);
        $_SESSION['username'] = preg_replace('/\s+/', '', $_SESSION['username']);
        $_SESSION['password'] = mysqli_real_escape_string($connection, $_POST['password']);
        $_SESSION['password'] = preg_replace('/\s+/', '', $_SESSION['password']);
        $_SESSION['user_table'] = hash('sha1', $_SESSION['username'] . $_SESSION['password']);
        $_SESSION['user_table'] = "a" . $_SESSION['user_table'];
        $_SESSION['password'] = hash('sha512', $_SESSION['password']);
    }
}

if(!function_exists('notify')) 
{
    function notify($notifyTitle, $notifyMessage) 
    {
        $html  = file_get_contents(__DIR__."/../templates/html/header.html");
        $html  = $html . file_get_contents(__DIR__."/../templates/html/failure.html");
        $html  = $html . file_get_contents(__DIR__."/../templates/html/footer.html");
        $html  = str_replace("{{title}}", $notifyTitle,$html);
        $html  = str_replace("{{message}}", $notifyMessage,$html);
        echo $html;
    }
}


if (!function_exists('login')) 
{
    function login($connection)
    {
        credit($connection);
        $checkLoginInUsers = mysqli_query($connection, "SELECT * FROM users WHERE username='" . $_SESSION['username'] . "' AND pass_word = '" . $_SESSION['password'] . "'");
        if (mysqli_num_rows($checkLoginInUsers) == 1) 
        {
            mysqli_fetch_array($checkLoginInUsers);
            $_SESSION['loggedin'] = 1;
            $checkGroup = mysqli_query($connection, "SELECT * FROM groups WHERE username='".$_SESSION['username']."' AND usertype='admin'");
            if(!empty($checkGroup)&&mysqli_num_rows($checkGroup)==1)
            {
                $_SESSION['usertype'] = "admin";
                mysqli_query($connection, "CREATE TABLE fccr.".$_SESSION['username']."(corporation VARCHAR(767) UNIQUE PRIMARY KEY, database_token VARCHAR(767))");
            }
            else
            {
                $userTypeArray = mysqli_query($connection, "SELECT * FROM groups WHERE username='".$_SESSION['username']."'");
                if(!empty($userTypeArray))
                {
                    $userTypeRow = mysqli_fetch_array($userTypeArray);
                    $_SESSION['usertype'] = $userTypeRow[1];
                }
                else
                    $_SESSION['usertype'] = "usertype1";
            }
            header("Location: http://localhost:".$_SERVER['SERVER_PORT']."/public/session.php");
        } 
        else
            notify("Error","Wrong Credentials");  
    }
}

if (!function_exists('register')) 
{
    function register($connection)
    {
        credit($connection);
        $checkusername = mysqli_query($connection, "SELECT * FROM groups WHERE username='" . $_SESSION['username'] . "'");
        if (mysqli_num_rows($checkusername) == 1) 
        {
            $checkusernameInUsers = mysqli_query($connection, "SELECT * FROM users WHERE username='" . $_SESSION['username'] . "'");
            if (mysqli_num_rows($checkusernameInUsers) == 1) 
            {
                notify("Error","Credentials already in use!");
                header("Refresh:5");
            } 
            else 
            {
                $registerquery = mysqli_query($connection, "INSERT INTO users (username,pass_word) VALUES('" . $_SESSION['username'] . "','" . $_SESSION['password'] . "')");
                if ($registerquery) 
                {
                    $r = mysqli_query($connection, "CREATE TABLE fccr.". $_SESSION['user_table'] ."(assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE);");
                    notify("Success","Your account was successfully created. You're being redirected to the login page");
                    sleep(2);
                    header("Location: http://localhost:".$_SERVER['SERVER_PORT']."/public/login.php");
                } 
                else 
                    notify("Error","Sorry, your registration failed. Please go back and try again1.");
            }
        } 
        else 
        {
            mysqli_query($connection, "INSERT INTO groups (username, usertype) VALUES('" . $_SESSION['username'] . "','usertype1')");
            $registerquery = mysqli_query($connection, "INSERT INTO users (username,pass_word) VALUES('" . $_SESSION['username'] . "','" . $_SESSION['password'] . "')");
            if ($registerquery)
            {
                $r = mysqli_query($connection, "CREATE TABLE fccr.". $_SESSION['user_table'] ."(assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE)");
                notify("Success","Your account was successfully created. You're being redirected to the login page");
                sleep(2);
                header("Location: http://localhost:".$_SERVER['SERVER_PORT']."/public/login.php");
            } 
            else
                notify("Error","Sorry, your registration failed. Please go back and try again.");
        }
    }
}

if (!function_exists('populate_user_data')) 
{
    function populate_user_data($connection)
    {
        /** Presentation Logic: populate_user_data **/
        $html = file_get_contents(__DIR__."/../templates/html/user.html");
        $html = str_replace("{{regularUser}}", $_SESSION['username'], $html);
        $user_data = array();
        $user_data = mysqli_query($connection, "SELECT * FROM ".$_SESSION['user_table'].";");
        if (!$user_data)
            $html = str_replace("{{regularUserAssetsTable}}","You have no assets yet!", $html);
        else 
        { 
            $table = array();
            for($i = 0; $i < mysqli_num_rows($user_data);  $i++)
            {
                $user_data_row =  mysqli_fetch_array($user_data);
                array_push($table,$user_data_row[0]);
                array_push($table,$user_data_row[1]);
            }
            $html = str_replace("{{regularUserAssetsTable}}", Regina::createTable(array("Asset Name", "Asset Location"),$table), $html); 
        }



        /** Hybrid Logic: Respond to Inspection **/
        $inspection_admins = mysqli_query($connection, "SELECT * FROM groups WHERE usertype='admin'");
        if (!empty($inspection_admins)&&!mysqli_num_rows($inspection_admins))
            $html = str_replace("{{inspectionRequest}}","No Admins! Oh it's chaos :D",$html);
        else while ($inspection_admins_onebyone = mysqli_fetch_array($inspection_admins)) 
        {
            $inspection_requests = mysqli_query($connection, "SELECT * FROM ".$inspection_admins_onebyone[0]." WHERE corporation = '" . $_SESSION['username'] . "'");
            if (!mysqli_num_rows($inspection_requests))
                $html = str_replace("{{inspectionRequest}}","No inspections! Oh joy! *_*",$html);
            else while ($respond_to_request = mysqli_fetch_array($inspection_requests)) 
            {
                if ($respond_to_request[1] == '0')
                {
                    $inspection_granted = mysqli_query($connection, "UPDATE " . $inspection_admins_onebyone[0] . " SET database_token = '" . $_SESSION['user_table'] . "' WHERE corporation = '" . $_SESSION['username'] . "'");
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
    function insert_user_data($connection)
    {
        /** Business Logic: insert_user_data **/
        if (!empty($_POST['assetname']) && !empty($_POST['assetcoordinates'])) 
        {
            $checkServices = mysqli_query($connection, "SELECT * FROM services where usertype='".$_SESSION['usertype']."'");
            if(!empty($checkServices))
            {
                if(mysqli_fetch_array($checkServices)[1]=="accessGranted")
                {
                    $user_data_inserted = mysqli_query($connection, "INSERT INTO ".$_SESSION['user_table']."(assetname,assetcoordinates) VALUES('" . $_POST['assetname'] . "', '" . $_POST['assetcoordinates'] . "')");
                    if ($user_data_inserted == 1)
                        header("Refresh:0");
                }
            }
        }
    }
}


if (!function_exists('populate_admin_area')) 
{
    function populate_admin_area($connection)
    {
        $corporationListTable1 = array();
        $corporationListTable2 = array();
        $html = file_get_contents(__DIR__."/../templates/html/admin.html");
        $html = str_replace("{{adminUser}}", $_SESSION['username'], $html);
        $admin_data = mysqli_query($connection, "SELECT * FROM groups");
        if (!mysqli_num_rows($admin_data))
            $html = str_replace("{{regularUsersTable}}", "Unfortunately there seems to be no corporations on record, peace failed and the world was destroyed :)", $html);
        else
        {
            for($i = 0; $i < mysqli_num_rows($admin_data);  $i++)
            {
                $user_data_array =  mysqli_fetch_array($admin_data);
                if ($user_data_array[1] == "usertype1"||$user_data_array[1] == "usertype2")
                {
                    array_push($corporationListTable1,$user_data_array[0]);
                    array_push($corporationListTable2,$user_data_array[0]);
                    array_push($corporationListTable2,$user_data_array[1]);
                }
            }
            $html = str_replace("{{regularUsersTable}}", Regina::createTable(array("Corporation Name","Group"),$corporationListTable2), $html); 

        }

        $html = str_replace("{{corporationSelect}}", Regina::createSelect("corporationSelect",$corporationListTable1), $html);

        $userAssetTable = array();
        $inspection_rights = mysqli_query($connection, "SELECT * FROM " . $_SESSION['username']);
        if (!mysqli_num_rows($inspection_rights))
            array_push($userAssetTable,"No inspection rights granted yet");
        else while ($inspection_rights_array = mysqli_fetch_array($inspection_rights)) 
        {
            array_push($userAssetTable,$inspection_rights_array[0]);
            $inspection_granted_data = mysqli_query($connection, "SELECT * FROM " . $inspection_rights_array[1]);
            if (mysqli_num_rows($inspection_granted_data))
            { 
                $tempTable = array();
                for($i = 0; $i < mysqli_num_rows($inspection_granted_data);  $i++)
                {
                    $inspection_granted_data_array = mysqli_fetch_array($inspection_granted_data);
                    array_push($tempTable,$inspection_granted_data_array[0]);
                    array_push($tempTable,$inspection_granted_data_array[1]);
                }
                array_push($userAssetTable, Regina::createTable(array("Asset Name","Asset Location"),$tempTable));
                mysqli_query($connection, "DELETE FROM " . $_SESSION['username'] . " WHERE database_token != '0'");
            }
        }
        $html = str_replace("{{inspectionTable}}", Regina::createTable(array("Corporation"),$userAssetTable), $html);
        $html = str_replace("{{selectCorporation}}", Regina::createSelect("selectCorporation",$corporationListTable1), $html);
        echo $html;
    }
}

if (!function_exists('inspect_user_data')) 
{
    function inspect_user_data($connection)
    {
        if(!empty($_POST['corporationSelect'])&&isset($_POST['corporationSelect']))
        {
            $username = $_SESSION['username'];
            $usertoinspect = $_POST['corporationSelect'];
            $usertoinspect = mysqli_real_escape_string($connection, $usertoinspect);
            $usertoinspect = preg_replace('/\s+/', '', $usertoinspect);
            if (!empty($username) && !empty($usertoinspect)) 
            {
                $inspection_requested = mysqli_query($connection, "INSERT INTO fccr.$username (corporation,database_token) VALUES('$usertoinspect','0')");
                header('Refresh:0');
            }
        }
    }
}


if(!function_exists('change_group_permissions'))
{
    function change_group_permissions($connection)
    {
        if(!empty($_POST['selectUserType'])&&!empty($_POST['accessType']))
        {
            $access = $_POST['accessType'];
            mysqli_query($connection, "UPDATE services set service='$access' WHERE usertype = '".$_POST['selectUserType']."'");
            header('Refresh:0');
        }
    }
}

if(!function_exists('change_user_group'))
{
    function change_user_group($connection)
    {
        if(!empty($_POST['selectCorporation'])&&!empty($_POST['setType']))
        {
            $newType = $_POST['setType'];
            mysqli_query($connection, "UPDATE groups set usertype='$newType' WHERE username = '".$_POST['selectCorporation']."'");
            header('Refresh:0');
        }
    }
}
?>
