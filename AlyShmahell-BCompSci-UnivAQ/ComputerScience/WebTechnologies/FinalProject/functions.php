<?php

if (!function_exists('login')) {
    function logIn($username,$password) {
	$username = mysql_real_escape_string($username);
	$username = preg_replace('/\s+/', '', $username);
	$password = hash('sha512',mysql_real_escape_string($password));
	$password = preg_replace('/\s+/', '', $password);
	$checkLoginInUsers = mysql_query("SELECT * FROM users WHERE username='".$username."' AND pass_word = '".$password."'");
        $checkLoginInAdmins = mysql_query("SELECT * FROM admins WHERE username='".$username."' AND pass_word = '".$password."'");
	if(mysql_num_rows($checkLoginInUsers)==1)
		{
			$row = mysql_fetch_array($checkLoginInUsers);
			$_SESSION['loggedin'] = 1;
			$_SESSION['username'] = $row[0];
			echo "<h1> success </h1>";
			echo "<p> Redirecting to Member Area </p>";
			echo '<script type="text/javascript"> window.location = "session.php" </script>';
		}
	else if(mysql_num_rows($checkLoginInAdmins)==1)
		{
			$row = mysql_fetch_array($checkLoginInAdmins);
			$_SESSION['loggedin'] = 1;
			$_SESSION['username'] = $username;
			echo "<h1> success </h1>";
			echo "<p> Redirecting to Member Area </p>";
			echo '<script type="text/javascript"> window.location = "session.php" </script>';
		}
	else
		{
			echo "<h1> Error </h1>";
			echo "<p> Wrong Credentials! </p>";
			echo $username;
		}
 }
}
?>
