import datetime
import string
import json
from time import sleep
import traceback
import mysql.connector

class MySQLDatabase:
    def __init__(self) -> None:
        self.db = None
    
    def connect(self, _host, _user, _password, _database, _it=0):
        try:
            self.db = mysql.connector.connect(
            host=_host,
            user=_user,
            password=_password,
            database=_database,
            autocommit=True
            )
            print("Connected !")
        except mysql.connector.errors.DatabaseError:
            if _it < 10:
                traceback.print_exc()
                print("Can't connect to database, retry in 10seconds...", _host, _user, _password, _database)
                sleep(10)
                self.connect(_host, _user, _password, _database, _it)
            else:
                print("Exiting!")
                return
        
    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%a %b %d %H:%M:%S %Y")
        
    def query(self, _query: string):
        if self.db:
            mycursor = self.db.cursor(dictionary=True, buffered=True)
            mycursor.execute(_query)
            if "SELECT" in _query or "SHOW" in _query:
                myresult = mycursor.fetchall()
                output = json.loads(json.dumps(list(myresult), default = self.myconverter))
            else:
                myresult = mycursor.lastrowid
                output = json.loads(json.dumps({"id": myresult}, default = self.myconverter))
            mycursor.close()
            return output
        else:
            raise Exception('Please connect the db first')
