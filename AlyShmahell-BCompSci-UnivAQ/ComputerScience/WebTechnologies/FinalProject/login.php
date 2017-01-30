<?php

include "header.php";

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    logIn($_POST['username'], $_POST['password']);
} else {
    ?>
    <h1>Member Login</h1>
    <p>you can either login below, or <a href="register.php">register</a>.</p>
    <form method="post" name="loginform" id="loginform">
            <label>Username: &nbsp</label><input type="text" name="username"/><br/>
            <label>Password: &nbsp</label><input type="password" name="password"/><br/>
            <input type="submit" name="login" value="Login"/>
    </form>
    <?php
}
?>
</div>
</body>
</html>
