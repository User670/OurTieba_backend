import sqlite3


conn = sqlite3.connect("test.db")
cursor = conn.cursor()

query = "CREATE TABLE user (id varchar(20) primary key, password varchar(200))"
cursor.execute(query)

query = "INSERT INTO user values ('0005', 'guess')"
cursor.execute(query)

query = "SELECT * FROM user"
cursor.execute(query)
data = cursor.fetchall()
print(data)

conn.commit()
cursor.close()
conn.close()