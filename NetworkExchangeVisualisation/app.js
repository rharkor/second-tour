var express = require('express')
var app = express()
var fs = require('fs')
var globalData = []

// Use json parser
app.use(express.json())

// Add the public folder to the server
app.use(express.static('public'))

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html')
})

app.post('/add', function (req, res) {
  let body = req.body
  // Parse the data
  let dataJson = globalData
  // Put id to the body
  body.id = dataJson.length
  // Add the new item to the array
  console.log(body)
  if (body.type && body.name) {
    dataJson.push(body)
    globalData = dataJson
    res.send('Item added')

  }
})

app.get('/data', function (req, res) {
  res.send(globalData)
})

var server = app.listen(3000, function () {
  let port = server.address().port
  console.log('Example app listening on port %s', port)
})
