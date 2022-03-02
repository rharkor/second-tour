const mysql = require('mysql')
require('../libs/strftime')

class MySQLDatabase {
  constructor () {
    this.db = null
  }

  async connect (_host, _user, _password, _database, _it = 0) {
    try {
      this.db = mysql.createConnection({
        host: _host,
        user: _user,
        password: _password,
        database: _database,
        autocommit: true
      })
      let result = await new Promise((resolve,reject)=>{
        this.db.connect((err) => {
          if(err){
            resolve(false);
          }else{
            resolve(true);
          }
        });
      })
      if (result){
      console.log("Connected !")
      }else{
        throw "Error in the connection with the db"
      }
    } catch (e) {
      if (_it < 10) {
        console.log(
          "Can't connect to database, retry in 10seconds...",
          _host,
          _user,
          _password,
          _database
        )
        await new Promise(r => setTimeout(r, 10000))
        this.connect(_host, _user, _password, _database, _it)
      } else {
        console.log('Exiting!')
        return
      }
    }
  }

  myconverter (key, value) {
    if (this[key] instanceof Date) {
      // .strftime("%a %b %d %H:%M:%S %Y")
      return strftime('%a %b %d %H:%M:%S %Y', this[key])
    }

    return value
  }

  async query (_query) {
    if (this.db) {
      return new Promise((resolve, reject) => {
        this.db.query(_query, (err, result, fields) => {
          if (err) {
            return reject(err)
          } else {
            let output
            if (
              _query.indexOf('SELECT') != -1 ||
              _query.indexOf('SHOW') != -1
            ) {
              output = JSON.parse(JSON.stringify(result, this.myconverter))
            } else {
              let myresult = result['insertId']
              output = JSON.parse(
                JSON.stringify({ id: myresult }, this.myconverter)
              )
            }
            resolve(output)
          }
        })
      })
      // mycursor = this.db.cursor(dictionary=true, buffered=true)
      // mycursor.execute(_query)
      // if (_query.indexOf("SELECT") != -1 || _query.indexOf("SHOW") != -1){
      //     myresult = mycursor.fetchall()
      //     output = JSON.parse(JSON.stringify(list(myresult), this.myconverter))
      // }else{
      //     myresult = mycursor.lastrowid
      //     output = JSON.parse(JSON.stringify({"id": myresult}, this.myconverter))
      // mycursor.close()
      // return output
      // }
    } else {
      throw 'Please connect the db first'
    }
  }
}

module.exports = MySQLDatabase
