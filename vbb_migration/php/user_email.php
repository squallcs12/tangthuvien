<?php
error_reporting(0);

if($_GET['code'] != '123qweasdzxc'){
	die; //security check
}

$vbbRoot = "/home/www/tangthuvien.com/public_html/forum";

require_once "{$vbbRoot}/includes/config.php";

$connect = mysql_connect($config['MasterServer']['servername'], $config['MasterServer']['username'], $config['MasterServer']['password']);
mysql_select_db($config['Database']['dbname']);

define('TABLE_PREFIX', $config['Database']['tableprefix']);


$username = $_GET['username']; //daotranbang

$sql = "SELECT email FROM `".TABLE_PREFIX."user` WHERE username='" . mysql_real_escape_string($username) . "' LIMIT 1";
$result = mysql_query($sql) or die();
$user = mysql_fetch_assoc($result);
mysql_free_result($result);
die($user['email']);
