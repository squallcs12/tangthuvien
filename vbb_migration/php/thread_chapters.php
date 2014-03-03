<?php
require_once "init.php";


$threadId = $_GET['threadid']; // 12
$page = $_GET['page']; // 1
$each = 10;
$start = ($page - 1) * $each;

if(!$page){
    $sql = "SELECT count(*) FROM `".TABLE_PREFIX."post` WHERE threadid='" . mysql_real_escape_string($threadId) . "'";
    $result = mysql_query($sql) or die(mysql_error());
    $row = mysql_fetch_row($result);
    die(ceil($row[0] / $each));
}

$sql = "SELECT * FROM `".TABLE_PREFIX."post` WHERE threadid='" . mysql_real_escape_string($threadId) . "' LIMIT $start, $each";
$result = mysql_query($sql) or die(mysql_error());

$posts = array();
while($post = mysql_fetch_assoc($result))
    $posts[] = $post;

header("Content-type: application/json; charset=utf-8");

die(json_encode($posts));