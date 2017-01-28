<?php 

include "header.php";

if(!empty($_POST['username']) && !empty($_POST['password']))
   {
		$username = mysql_real_escape_string($_POST['username']);
		$password = hash('sha512',mysql_real_escape_string($_POST['password']));
		$checklogin = mysql_query("SELECT * FROM users WHERE username='".$username."' AND password = '".$password."'");
		if(mysql_num_rows($checklogin)==1)
                   {
			$row = mysql_fetch_array($checklogin);
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
                        echo $password;
		   }
  }
else
  {
    ?>
    <h1>Member Login</h1>
    <p>you can either login below, or <a href="register.php">register</a>.</p>
    <form method="post" action="index.php" name="loginform" id="loginform">
      <fieldset>
        <label for="username">Username:</label><input type="text" name="username" id="username" /><br />
        <label for="password">Password:</label><input type="password" name="password" id="password" /><br />
        <input type="submit" name="login" id="login" value="Login" />
      </fieldset>
    </form>
    <?php
  }
?>
</div>
</body>
</html>
