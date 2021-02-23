<html>
<head>
	<title>db test</title>
</head>
<body>
<h1>db test</h1>
<div>
<?php
//$link = mysql_connect('172.18.0.2', 'root', 'my-secret-pw')
//    or die('Не удалось соединиться: ' . mysql_error());
$mysqli = new mysqli("mysql-db", "root", "my-secret-pw", "mysql");
if ($mysqli->connect_errno) {
    echo "Не удалось подключиться к MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
} else {
echo 'Соединение успешно установлено!!!<br>';
}

$res = $mysqli->query("SHOW DATABASES");
for ($row_no = $res->num_rows - 1; $row_no >= 0; $row_no--) {
    $res->data_seek($row_no);
    $row = $res->fetch_assoc();
    echo " id = " . $row['Database'] . "<br>";
}

?>
</div>
</body>
</html>
