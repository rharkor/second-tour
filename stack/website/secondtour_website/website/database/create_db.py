import os
import traceback
import mysql.connector

try: 
    mydb = mysql.connector.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        passwd = os.getenv('DB_PWD'),
    )

    my_cursor = mydb.cursor()

    #my_cursor.execute("CREATE DATABASE dbSecondTour")

    my_cursor.execute("SHOW DATABASES")
    for db in my_cursor : 
        print(db)
except Exception:
    traceback.print_exc()