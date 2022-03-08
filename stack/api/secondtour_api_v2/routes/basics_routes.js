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

/**
 * @swagger
 * /{table}:
 *    post:
 *      tags:
 *          - Automated Data Operation
 *      description: Return all the rows of a table
 *      parameters:
 *          - in: path
 *            name: table
 *            type: string
 *            required: true
 *            description: The table you want to fetch
 *          - in: body
 *            name: User auth
 *            type: object
 *            schema:
 *              $ref: '#definitions/User'
 *      responses:
 *          '200':
 *              description: Table retreive correctly
 *              schema:
 *                  $ref: '#definitions/fetchOut'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
 router.route('/:table').post(async (req, res) => {
  let table = req.params['table']
  let result = await db.query(`SELECT * FROM ${table};`).catch(e => {
    res.status(500).send(e)
  })
  res.send(result)
})