import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost",
							user = "root",
							passwd = "mario",
							db = "projetox")
	c = conn.cursor()

	return c, conn 