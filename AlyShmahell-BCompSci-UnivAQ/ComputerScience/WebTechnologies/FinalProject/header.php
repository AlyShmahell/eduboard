<?php include "db_connect.inc.php"; ?>
<?php include "functions.php"; ?>

<!DOCTYPE HTML>
<html>
    <head>
        <title>FCCR</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <link href="bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css" />
        <link href="bootstrap/css/bootstrap-responsive.css" rel="stylesheet" type="text/css" />

        <style>
            @font-face {
                font-family: 'spaceship';
                src: url("bootstrap/fonts/Spaceship-Bullet.ttf");
            }

            @font-face {
                font-family: 'glyphicons-halflings-regular';
                src: url("bootstrap/fonts/glyphicons-halflings-regular.ttf");
            }
            body {
                font-family: 'glyphicons-halflings-regular';
                text-align:center;
            }
            h1, h2, h3 {
                font-family: 'spaceship';
            }

            input[type="text"], input[type="password"] {
                text-align:center;
                border: solid transparent;
                outline:none
                    background-color:#ffffff;
                text-decoration:none;
            }
            input[type="submit"] {
                border: solid transparent;
                background-color: gainsboro;
                color:#428bca;
            }
            div {
                border-top: groove black;
                text-align: center;
                padding: 10px;
                margin-left: 200px;
                margin-right: 200px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
            table, tr, th, td {
                border: solid black;
                margin: 0 auto;
                padding: 5px;
            }
        </style>
    </head>
    <body>

