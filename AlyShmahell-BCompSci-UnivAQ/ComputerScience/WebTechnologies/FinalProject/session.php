<?php include "header.php"; include "functions.php"; ?>
<?php if($_SESSION['usertype']=="user") {?> <h1>Corporation Area</h1> <?php } else if($_SESSION['usertype']=="admin") {?>
<h1>Administration Area</h1>
<?php } ?>
<div><p> Welcome <?php echo $_SESSION['username'];  ?> </p></div>

<?php if($_SESSION['usertype']=="user") {populate_user_data();respond_to_inspection();} else if($_SESSION['usertype']=="admin") {populate_admin_area();} ?>

<?php
if($_SESSION['usertype']=="user")  {insert_user_data(); ?>
<div>
<form method="post" name="insert-user-data">
<label>asset name</label><input type="text" name="assetname"><br/>
<label>asset coordinates</label><input type="text" name="assetcoordinates"><br/>
<input type="submit">
</form>
</div>
<div>
<p><a href="logout.php">click here to logout</a></p>
</div>
</body>
</html>
<?php } else {inspect_user_data(); ?>
<div>
<h4> Corporation Ispection Form </h4>
<form method="post" name="inspectuserdata">
<label>corporation name</label><input type="text" name="usertoinspect"><br/>
<input type="submit">
</form>
</div>
<div>
<p><a href="logout.php">click here to logout</a></p>
</div>
</body>
</html>
<?php }  ?>
