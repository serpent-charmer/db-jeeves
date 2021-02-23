import pymysql.cursors


connection = pymysql.connect(host='172.18.0.2',
                             user='root',
                             password='my-secret-pw',
                             database='mysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection:
	with connection.cursor() as cursor:
		# Create a new record
		cursor.execute('SHOW DATABASES')
		print(cursor.fetchall())
