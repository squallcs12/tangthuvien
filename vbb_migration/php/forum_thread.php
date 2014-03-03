<?php
require_once "init.php";

$fid = $_REQUEST['fid'];
$page = $_REQUEST['p'];
$each = 10;
$start = $page * $each - $each;


$sql = "SELECT * FROM `".TABLE_PREFIX."thread` WHERE forumid='" . mysql_real_escape_string($fid) . "'  ORDER BY dateline ASC LIMIT $start, $each";

$result = mysql_query($sql) or die(mysql_error());

$threads = array();
while($thread = mysql_fetch_assoc($result))
    $threads[] = $thread;

header("Content-type: application/json; charset=utf-8");

die(json_encode($threads));