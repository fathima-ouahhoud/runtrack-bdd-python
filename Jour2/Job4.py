import mysql.connector

conn = mysql.connector.connect(
            host="localhost",
            user="root", 
            password=".env", 
            database="laplateforme"
        )
cursor = conn.cursor()


cursor.execute("SELECT nom, capacite FROM salle")
result = cursor.fetchall()
print(result)

conn.close()
