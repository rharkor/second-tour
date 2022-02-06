import datetime
import string
from itsdangerous import json
import mysql.connector

class MySQLDatabase:
    def __init__(self) -> None:
        self.db = None
    
    def connect(self, _host, _user, _password, _database):
        self.db = mysql.connector.connect(
        host=_host,
        user=_user,
        password=_password,
        database=_database
        )
        
    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%a %b %d %H:%M:%S %Y")
        
    def query(self, _query: string):
        if self.db:
            mycursor = self.db.cursor(dictionary=True)
            mycursor.execute(_query)
            if "SELECT" in _query:
                myresult = mycursor.fetchall()
                output = json.loads(json.dumps(list(myresult), default = self.myconverter))
            else:
                myresult = mycursor.lastrowid
                output = json.loads(json.dumps({"id": myresult}, default = self.myconverter))
            return output
        else:
            raise Exception('Please connect the db first')
