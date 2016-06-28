import sqlite3

with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE posts")
	c.execute("CREATE TABLE usuarios(title TEXT, description TEXT)")
	c.execute('INSERT INTO usuarios VALUES("Mario", "Im The flash.")')
	c.execute('INSERT INTO usuarios VALUES("Arrow", "Im Oliver Queen.")')
