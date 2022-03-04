const express = require('express')
const router = express.Router()
const test_connection = require('../security/main_security')

// Middleware
router.use('/*', (req, res, next) => {
  if (test_connection(req.body)) {
    next()
  } else {
    res.status(401).send('Invalid auth : ' + req.body.username)
  }
})