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
        if (mysql_num_rows($checkLoginInUsers) == 1)
		{
            $row = mysql_fetch_array($checkLoginInUsers);
            $_SESSION['loggedin'] = 1;
            $_SESSION['username'] = $row[0];
            $_SESSION['user_db'] = hash('sha256', $username + $password);
            echo "<h1> success </h1>";
            echo "<p> Redirecting to Member Area </p>";
            echo '<script type="text/javascript"> window.location = "session.php" </script>';
        }
	else if (mysql_num_rows($checkLoginInAdmins) == 1) {
        $row = mysql_fetch_array($checkLoginInAdmins);
        $_SESSION['loggedin'] = 1;
        $_SESSION['username'] = $username;
        $_SESSION['user_db'] = hash('sha256', $username + $password);
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
                    mysql_query("CREATE TABLE $user_db (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,email VARCHAR(50),reg_date TIMESTAMP)");
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
                mysql_query("CREATE TABLE $user_db (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, firstname VARCHAR(30) NOT NULL,lastname VARCHAR(30) NOT NULL,email VARCHAR(50),reg_date TIMESTAMP)");
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
    function populate_user_data() {
             echo "<br/>";
             $user_db = $_SESSION['user_db'];
             $user_data = mysql_query("SELECT * FROM $user_db");
             $user_data = mysql_fetch_array($user_data);
             if(mysql_num_rows($user_data)==0)
                        echo "You have no assets yet!";
             foreach($row as $value) {
                        echo $value;
  }
 }
}
if (!function_exists('insert_user_data')) {
    function insert_user_data() {
             echo "<br/>";
             $user_db = $_SESSION['user_db'];
             $user_data = mysql_query("SELECT * FROM $user_db");
             $user_data = mysql_fetch_array($user_data);
             if(mysql_num_rows($user_data)==0)
                        echo "You have no assets yet!";
             foreach($row as $value) {
                        echo $value;
  }
 }
}
?>
