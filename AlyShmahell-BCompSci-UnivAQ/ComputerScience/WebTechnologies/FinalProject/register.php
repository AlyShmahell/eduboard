<?php include "header.php";
?>
<?php 
if (!empty($_POST['username']) && !empty($_POST['password'])) {
    register($_POST['username'], $_POST['password']);
} else {
    ?>
    <h1>Register</h1>
    <div>
    <?php echo "If you already have your corporation on record, please";?> <a href="login.php">login</a>.</p>
    </div>
    <div>
    <p>if not, please enter your details below to register.</p>
    <form method="post" action="register.php" name="registerform" id="registerform">
        <fieldset>
            <label for="username">Username:</label><input type="text" name="username" id="username"/><br/>
            <label for="password">Password:</label><input type="password" name="password" id="password"/><br/>
            <input type="submit" name="register" id="register" value="Register"/>
        </fieldset>
    </form>
    </div>
    <?php
}
?>
</div>
</body>
</html>
