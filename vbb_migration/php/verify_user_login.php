<?php
require_once "init.php";


$username = $_GET['username']; //daotranbang
$password = $_GET['password']; //

$sql = "SELECT userid, username, email, password, salt FROM `".TABLE_PREFIX."user` WHERE username='" . mysql_real_escape_string($username) . "' LIMIT 1";
$result = mysql_query($sql) or die(mysql_error());
$user = mysql_fetch_assoc($result);
mysql_free_result($result);

if($user['password'] == md5(md5($password) . $user['salt'])){
    die(json_encode($user));
}
die("0");


