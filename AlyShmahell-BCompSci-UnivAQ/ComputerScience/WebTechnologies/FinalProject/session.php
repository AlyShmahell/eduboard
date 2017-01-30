<?php include "header.php"; include "functions.php"; ?>
<h1>Corporation Area</h1>
<div>
<p> Welcome <?php session_start(); echo $_SESSION['username']; populate_user_data();?> </p>
</div>
<div>
<?php insert_user_data(); ?>
<form method="post" name="insert-user-data">
<label>asset name</label><input type="text" name="assetname"><br/>
<label>asset coordinates</label><input type="text" name="assetcoordinates"><br/>
<input type="submit">
</form>
</div>
<div>
<p><a href="logout.php">click here to logout</a></p>
</div>
</html>

