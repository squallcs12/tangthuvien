<?php
require_once "init.php";


$username = $_GET['username']; //daotranbang

$sql = "SELECT email FROM `".TABLE_PREFIX."user` WHERE username='" . mysql_real_escape_string($username) . "' LIMIT 1";
$result = mysql_query($sql) or die();
$user = mysql_fetch_assoc($result);
mysql_free_result($result);
die($user['email']);
