<?php include "header.php"; include "functions.php"; ?>
<h1>Corporation Area</h1>
<div>
<p> Welcome <?php session_start(); echo $_SESSION['username']; populate_user_data();?> </p>
<p><a href="logout.php">click here to logout</a></p>
</div>
</html>

