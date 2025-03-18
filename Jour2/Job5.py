import mysql.connector

conn = mysql.connector.connect(
            host="localhost",
            user="root", 
            password=".env", 
            database="laplateforme"
        )
cursor = conn.cursor()

cursor.execute("SELECT nom, capacite FROM salle")
resultat = cursor.fetchall()
print(resultat)
conn.close()
