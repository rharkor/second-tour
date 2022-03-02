const MySQLDatabase = require("./main_database")

DB_HOST = process.env.DB_HOST || 'localhost'
DB_USER = process.env.DB_USER || 'root'
DB_PWD = process.env.DB_PWD || ''
DB_NAME = process.env.DB_NAME || 'secondtour'

db = new MySQLDatabase()
db.connect(DB_HOST, DB_USER, DB_PWD, DB_NAME)

module.exports = db