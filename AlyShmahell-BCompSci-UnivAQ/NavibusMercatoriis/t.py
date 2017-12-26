import mysql.connector

config = {
  'user': 'root',
  'password': 'toor',
  'host': '127.0.0.1',
  'database': 'e',
  'raise_on_warnings': True,
}

cnx = mysql.connector.connect(**config)

cnx.close()
