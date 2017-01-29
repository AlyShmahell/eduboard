<?php 

include "header.php";

if(!empty($_POST['username']) && !empty($_POST['password']))
	{
	 logIn($_POST['username'],$_POST['password']);	
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
