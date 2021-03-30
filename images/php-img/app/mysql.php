<html>
<head>
	<title>db test</title>
</head>
<body>
<h1>db test</h1>
<div>
<?php
$mysqli = new mysqli("mysql-db", getenv("DB_LOGIN"), getenv("DB_PWD"), getenv("DB_NAME"));
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
