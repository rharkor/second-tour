const mysql = require('mysql')
const axios = require('axios')

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
      let t = this
      this.db.on('error', function (err) {
        console.log('db error', err)
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
          t.connect(_host, _user, _password, _database, 0)
        } else {
          throw err
        }
      })
      let result = await new Promise((resolve, reject) => {
        this.db.connect(err => {
          if (err) {
            resolve(false)
          } else {
            resolve(true)
          }
        })
      })
      if (result) {
        console.log('Connected !')
        if (process.env.NETWORK_VISU == 'true') {
        axios
          .post('http://' + process.env.LOCAL_IP + ':3000/add', {
            type: 'node',
            name: 'mysql',
            data: {
              name: 'mysql',
              id: 'mysql',
              size: 123,
              fsize: 50
            },
            position: {
              x: 680,
              y: 90
            }
          })
          .catch(err => {
            console.log(err)
          })
      }
      } else {
        throw 'Error in the connection with the db'
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

function strftime (sFormat, date) {
  if (!(date instanceof Date)) date = new Date()
  var nDay = date.getDay(),
    nDate = date.getDate(),
    nMonth = date.getMonth(),
    nYear = date.getFullYear(),
    nHour = date.getHours(),
    aDays = [
      'Sunday',
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday'
    ],
    aMonths = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ],
    aDayCount = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
    isLeapYear = function () {
      return (nYear % 4 === 0 && nYear % 100 !== 0) || nYear % 400 === 0
    },
    getThursday = function () {
      var target = new Date(date)
      target.setDate(nDate - ((nDay + 6) % 7) + 3)
      return target
    },
    zeroPad = function (nNum, nPad) {
      return (Math.pow(10, nPad) + nNum + '').slice(1)
    }
  return sFormat.replace(/%[a-z]/gi, function (sMatch) {
    return (
      ({
        '%a': aDays[nDay].slice(0, 3),
        '%A': aDays[nDay],
        '%b': aMonths[nMonth].slice(0, 3),
        '%B': aMonths[nMonth],
        '%c': date.toUTCString(),
        '%C': Math.floor(nYear / 100),
        '%d': zeroPad(nDate, 2),
        '%e': nDate,
        '%F': date.toISOString().slice(0, 10),
        '%G': getThursday().getFullYear(),
        '%g': (getThursday().getFullYear() + '').slice(2),
        '%H': zeroPad(nHour, 2),
        '%I': zeroPad(((nHour + 11) % 12) + 1, 2),
        '%j': zeroPad(
          aDayCount[nMonth] + nDate + (nMonth > 1 && isLeapYear() ? 1 : 0),
          3
        ),
        '%k': nHour,
        '%l': ((nHour + 11) % 12) + 1,
        '%m': zeroPad(nMonth + 1, 2),
        '%n': nMonth + 1,
        '%M': zeroPad(date.getMinutes(), 2),
        '%p': nHour < 12 ? 'AM' : 'PM',
        '%P': nHour < 12 ? 'am' : 'pm',
        '%s': Math.round(date.getTime() / 1000),
        '%S': zeroPad(date.getSeconds(), 2),
        '%u': nDay || 7,
        '%V': (function () {
          var target = getThursday(),
            n1stThu = target.valueOf()
          target.setMonth(0, 1)
          var nJan1 = target.getDay()
          if (nJan1 !== 4) target.setMonth(0, 1 + ((4 - nJan1 + 7) % 7))
          return zeroPad(1 + Math.ceil((n1stThu - target) / 604800000), 2)
        })(),
        '%w': nDay,
        '%x': date.toLocaleDateString(),
        '%X': date.toLocaleTimeString(),
        '%y': (nYear + '').slice(2),
        '%Y': nYear,
        '%z': date.toTimeString().replace(/.+GMT([+-]\d+).+/, '$1'),
        '%Z': date.toTimeString().replace(/.+\((.+?)\)$/, '$1')
      }[sMatch] || '') + '' || sMatch
    )
  })
}

module.exports = MySQLDatabase
