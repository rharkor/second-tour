const express = require('express')
const router = express.Router()

/**
 * @swagger
 * /version:
 *    get:
 *      description: Return the version of the api
 *      responses:
 *          '200':
 *              description: Version correctly retreived
 */
router.route('/version').get((req, res) => {
    res.send({'version': "1.0.0"})
})

/**
 * @swagger
 * /{table}:
 *    post:
 *      tags:
 *          - Automated Data Operation
 *      description: Return all the rows of a table if no parameters, if parameters returns the row selected by the parameters
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
/*
 router.route('/:table').post(async (req, res) => {
 let table = req.params['table']
 let content = req.body['content']
 let condition = ''
 Object.keys(content).forEach((element, index) => {
   if (index != 0) condition += ' AND '
   if (
     content[element] === 'null' ||
     !isNaN(content[element]) ||
     content[element] === 'true' ||
     content[element] === 'false'
   )
     condition += element + ' = ' + content[element]
   else condition += element + " = '" + content[element] + "'"
 })
 let result = await db
   .query(`SELECT * FROM ${table} WHERE ${condition};`)
   .catch(e => {
     res.status(500).send(e)
   })
 res.send(result)
})
*/
/*
 router.route('/:table').post(async (req, res) => {
    console.log("here")
    let table = req.params['table']
    let result = await db.query(`SELECT * FROM ${table};`).catch(e => {
        res.status(500).send(e)
    })
    res.send("here")
  })*/
module.exports = router