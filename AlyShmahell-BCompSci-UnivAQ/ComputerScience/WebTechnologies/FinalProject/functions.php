<?php

if (!function_exists('login')) {
    function logIn($username, $password)
    {
        $username = mysql_real_escape_string($username);
        $username = preg_replace('/\s+/', '', $username);
        $password = hash('sha512', mysql_real_escape_string($password));
        $password = preg_replace('/\s+/', '', $password);
        $checkLoginInUsers = mysql_query("SELECT * FROM users WHERE username='" . $username . "' AND pass_word = '" . $password . "'");
        $checkLoginInAdmins = mysql_query("SELECT * FROM admins WHERE username='" . $username . "' AND pass_word = '" . $password . "'");
        if (mysql_num_rows($checkLoginInUsers) == 1) {
            $row = mysql_fetch_array($checkLoginInUsers);
            $_SESSION['loggedin'] = 1;
            $_SESSION['username'] = $row[0];
            $_SESSION['usertype'] = "user";
            $_SESSION['user_db'] = hash('sha256', $username + $password);
            echo "<h1> success </h1>";
            echo "<p> Redirecting to Member Area </p>";
            echo '<script type="text/javascript"> window.location = "session.php" </script>';
        } else if (mysql_num_rows($checkLoginInAdmins) == 1) {
            $row = mysql_fetch_array($checkLoginInAdmins);
            $_SESSION['loggedin'] = 1;
            $_SESSION['username'] = $username;
            $_SESSION['usertype'] = "admin";
            $admin_db = mysql_query("CREATE TABLE $username(corporation VARCHAR(767) UNIQUE PRIMARY KEY, database_token VARCHAR(767))");
            echo "<h1> success </h1>";
            echo "<p> Redirecting to Member Area </p>";
            echo '<script type="text/javascript"> window.location = "session.php" </script>';
        } else {
            echo "<h1> Error </h1>";
            echo "<p> Wrong Credentials! </p>";
        }
    }
}
if (!function_exists('register')) {
    function register($username, $password)
    {
        $username = mysql_real_escape_string($username);
        $username = preg_replace('/\s+/', '', $username);
        $password = hash('sha512', mysql_real_escape_string($password));
        $password = preg_replace('/\s+/', '', $password);
        $user_db = hash('sha256', $username + $password);
        $checkusername = mysql_query("SELECT * FROM groups WHERE username='" . $username . "'");
        if (mysql_num_rows($checkusername) == 1) {
            $checkusernameInAdmins = mysql_query("SELECT * FROM admins WHERE username='" . $username . "'");
            $checkusernameInUsers = mysql_query("SELECT * FROM users WHERE username='" . $username . "'");
            if (mysql_num_rows($checkusernameInAdmins) == 1 || mysql_num_rows($checkusernameInUsers) == 1) {
                echo "<h1> Error </h1>";
                echo "<p> Credentials already in use! </p>";
            } else {
                $registerquery = mysql_query("INSERT INTO users (username,pass_word) VALUES('" . $username . "','" . $password . "')");
                if ($registerquery) {
                    mysql_query("CREATE TABLE $user_db (assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE)");
                    echo "<h1>Success 1</h1>";
                    echo "<p>Your account was successfully created. Please <a href=\"index.php\">click here to login</a>.</p>";
                } else {
                    echo "<h1>Error</h1>";
                    echo "<p>Sorry, your registration failed. Please go back and try again.</p>";
                }
            }

        } else {
            mysql_query("INSERT INTO groups (username) VALUES('" . $username . "')");
            $registerquery = mysql_query("INSERT INTO users (username,pass_word) VALUES('" . $username . "','" . $password . "')");
            if ($registerquery) {
                mysql_query("CREATE TABLE $user_db (assetname VARCHAR(300) NOT NULL UNIQUE PRIMARY KEY, assetcoordinates VARCHAR(300) NOT NULL UNIQUE)");
                echo "<h1>Success 2</h1>";
                echo "<p>Your account was successfully created. Please <a href=\"index.php\">click here to login</a>.</p>";
            } else {
                echo "<h1>Error</h1>";
                echo "<p>Sorry, your registration failed. Please go back and try again.</p>";
            }
        }
    }
}

if (!function_exists('populate_user_data')) {
    function populate_user_data()
    {
        echo "<br/> here are the assets to which you have claim for!<br/>";
        $user_db = $_SESSION['user_db'];
        $user_data = mysql_query("SELECT * FROM $user_db");
        if (!mysql_num_rows($user_data))
            echo "You have no assets yet!";
        while ($user_data_array = mysql_fetch_array($user_data)) {
            echo $user_data_array[0] . " ";
            echo $user_data_array[1] . "<br/>";
        }
    }
}
if (!function_exists('insert_user_data')) {
    function insert_user_data()
    {
        echo "Asset Claim Form, please name the asset you wish to claim and specify its location below: <br/>";
        $user_db = $_SESSION['user_db'];
        if (!empty($_POST['assetname']) && !empty($_POST['assetcoordinates']))
            $user_data_inserted = mysql_query("INSERT INTO $user_db(assetname,assetcoordinates) VALUES('" . $_POST['assetname'] . "', '" . $_POST['assetcoordinates'] . "')");
        if ($user_data_inserted == 1) {
            header("Refresh:0");
        }
    }
}

if (!function_exists('populate_admin_area')) {
    function populate_admin_area()
    {
        echo "<br/> here are the corporations we have on record!<br/>";
        $admin_data = mysql_query("SELECT * FROM groups");
        if (!mysql_num_rows($admin_data))
            echo "Unfortunately there seems to be no corporations on record, peace failed and the world was destroyed :)";
        while ($user_data_array = mysql_fetch_array($admin_data)) {
            if ($user_data_array[1] == "user")
                echo $user_data_array[0] . " ";
        }

        $inspection_rights = mysql_query("SELECT * FROM " . $_SESSION['username']);
        if (!mysql_num_rows($inspection_rights))
            echo "No inspection rights granted yet";
        else while ($inspection_rights_array = mysql_fetch_array($inspection_rights)) {
            $inspection_granted_data = mysql_query("SELECT * FROM " . $inspection_rights_array[1]);
            if (!mysql_num_rows($inspection_granted_data))
                echo "No Assets claimed by this company";
            else while ($inspection_granted_data_array = mysql_fetch_array($inspection_granted_data)) {
                echo $inspection_granted_data_array[0] . " ";
                echo $inspection_granted_data_array[1] . "<br/>";
            }
              mysql_query("DELETE FROM " . $_SESSION['username']);
        }
    }
}

if (!function_exists('inspect_user_data')) {
    function inspect_user_data()
    {
        if(isset($_POST['usertoinspect']))
         {
          $username = $_SESSION['username'];
        $username = mysql_real_escape_string($username);
        echo $username . " is a chicken <br/>";
        $usertoinspect = $_POST['usertoinspect'];
        $usertoinspect = mysql_real_escape_string($usertoinspect);
        echo $usertoinspect . " is a chicken too <br/>";
        if (!empty($username) && !empty($usertoinspect)) {
            $inspection_requested = mysql_query("INSERT INTO webtech.$username(corporation,database_token) VALUES('$usertoinspect','0')");
            if ($inspection_requested)
                echo "user " . $_POST['usertoinspect'] . " was informed of inspection and asked to comply";
            else
                echo "operation failed " . $_POST['usertoinspect'] . "  was not inserted into ".$_SESSION['username'];
        }
      }
    }
}


if (!function_exists('respond_to_inspection')) {
    function respond_to_inspection()
    {
        echo "<br/> Inspection Requests:<br/>";
        $inspection_admins = mysql_query("SELECT * FROM admins");
        if (!mysql_num_rows($inspection_admins))
            echo "No Admins! Oh it's chaos :D";
        else while ($inspection_admins_onebyone = mysql_fetch_array($inspection_admins)) {
            $inspection_requests = mysql_query("SELECT * FROM ".$inspection_admins_onebyone[0]." WHERE corporation = '" . $_SESSION['username'] . "'");
            if (!mysql_num_rows($inspection_requests))
                echo "No inspections! Oh joy! :D";
            else while ($respond_to_request = mysql_fetch_array($inspection_requests)) {
                if ($respond_to_request[1] == '0')
                    $inspection_granted = mysql_query("UPDATE " . $inspection_admins_onebyone[0] . " SET database_token = '" . $_SESSION['user_db'] . "' WHERE corporation = '" . $_SESSION['username'] . "'");
                if ($inspection_granted)
                    echo "admin '" . $inspection_admins_onebyone[0] . "' was granted inspection rights";
            }
        }
    }
}
?>
