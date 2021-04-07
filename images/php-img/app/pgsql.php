<html>
<head>
	<title>db test</title>
</head>
<body>
<h1>db test</h1>
<div>
<?php
$login = getenv("DB_LOGIN");
$db = getenv("DB_NAME");
$pwd = getenv("DB_PWD");

$dbconn = pg_pconnect("host=pgsql-db1 dbname=$db user=$login password=$pwd") or die("Error connecting to database" . pg_last_error());

?>
</div>
</body>
</html>
