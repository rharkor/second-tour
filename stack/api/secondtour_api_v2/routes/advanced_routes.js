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
 * /data/fetch/{table}:
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
router.route('/fetch/:table').post(async (req, res) => {
  let table = req.params['table']
  let result = await db.query(`SELECT * FROM ${table};`).catch(e => {
    res.status(500).send(e)
  })
  res.send(result)
})

/**
 * @swagger
 * /data/fetchfilter/{table}:
 *    post:
 *      tags:
 *          - Automated Data Operation
 *      description: Return all the rows of a table that match with your filter
 *      parameters:
 *          - in: path
 *            name: table
 *            type: string
 *            required: true
 *            description: The table you want to fetch
 *          - in: body
 *            name: User auth + Filter
 *            type: object
 *            schema:
 *              $ref: '#definitions/UserContentTableDescription'
 *      responses:
 *          '200':
 *              description: Table retreive correctly
 *              schema:
 *                  $ref: '#definitions/fetchFilterOut'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/fetchfilter/:table').post(async (req, res) => {
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

/**
 * @swagger
 * /data/fetchmulti:
 *    post:
 *      tags:
 *          - Automated Data Operation
 *      description: Return all the table and rows you asked
 *      parameters:
 *          - in: body
 *            name: User auth + Rows name
 *            type: object
 *            schema:
 *              $ref: '#definitions/UserContentTableName'
 *      responses:
 *          '200':
 *              description: Table retreive correctly
 *              schema:
 *                  $ref: '#definitions/fetchMultiOut'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/fetchmulti').post(async (req, res) => {
  let tables = req.body['content']
  let result = []
  for (let i = 0; i < tables.length; i++) {
    let table = tables[i]
    let a_result = await db.query(`SELECT * FROM ${table};`).catch(e => {
      res.status(500).send(e)
    })
    result.push(a_result)
  }

  res.send(result)
})

/**
 * @swagger
 * /data/insert/{table}:
 *    put:
 *      tags:
 *          - Automated Data Operation
 *      description: Insert a row in the table selected
 *      parameters:
 *          - in: path
 *            name: table
 *            type: string
 *            required: true
 *            description: The table you want to insert in the row
 *          - in: body
 *            name: User auth + Row content
 *            type: object
 *            schema:
 *              $ref: '#definitions/UserContentTableDescriptionFull'
 *      responses:
 *          '201':
 *              description: Table created successfully
 *              schema:
 *                  $ref: '#definitions/returnId'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/insert/:table').put(async (req, res) => {
  let table = req.params['table']
  let content = req.body['content']
  let values = '('
  Object.keys(content).forEach((element, index) => {
    values += element
    if (index != Object.keys(content).length - 1) values += ', '
  })
  values += ') VALUES ('
  Object.keys(content).forEach((element, index) => {
    if (content[element].toString().match(/... ... [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}/)) {
      content[element] =
        "STR_TO_DATE('" + content[element] + "', '%a %b %d %H:%i:%s %Y')"
      values += content[element]
    } else {
      if (
        content[element] === 'null' ||
        !isNaN(content[element]) ||
        content[element] === 'true' ||
        content[element] === 'false'
      )
        values += content[element]
      else values += "'" + content[element] + "'"
    }
    if (index != Object.keys(content).length - 1) values += ', '
  })
  values += ')'
  let result = await db.query(`INSERT INTO ${table} ${values};`).catch(e => {
    res.status(500).send(e)
  })
  res.status(201).send(result)
})

/**
 * @swagger
 * /data/delete/{table}:
 *    delete:
 *      tags:
 *          - Automated Data Operation
 *      description: Delete all the rows in the table you want
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
 *          '202':
 *              description: Table deleted succesfully
 *              schema:
 *                  $ref: '#definitions/returnId'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/delete/:table').delete(async (req, res) => {
  let table = req.params['table']
  let result = await db.query(`DELETE FROM ${table};`).catch(e => {
    res.status(500).send(e)
  })
  res.status(202).send(result)
})

/**
 * @swagger
 * /data/deletefilter/{table}:
 *    delete:
 *      tags:
 *          - Automated Data Operation
 *      description: Delete all the rows of a table that match with your filter
 *      parameters:
 *          - in: path
 *            name: table
 *            type: string
 *            required: true
 *            description: The table you where you want to delete rows
 *          - in: body
 *            name: User auth + Filter
 *            type: object
 *            schema:
 *              $ref: '#definitions/UserContentTableDescription'
 *      responses:
 *          '202':
 *              description: Rows successfully deleted
 *              schema:
 *                  $ref: '#definitions/returnId'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/deletefilter/:table').delete(async (req, res) => {
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
    .query(`DELETE FROM ${table} WHERE ${condition};`)
    .catch(e => {
      res.status(500).send(e)
    })
  res.status(202).send(result)
})

/**
 * @swagger
 * /data/deleteall:
 *    post:
 *      tags:
 *          - Automated Data Operation
 *      description: Delete all the rows of all the tables
 *      parameters:
 *          - in: body
 *            name: User auth
 *            type: object
 *            schema:
 *              $ref: '#definitions/User'
 *      responses:
 *          '202':
 *              description: Rows successfully deleted
 *              schema:
 *                  $ref: '#definitions/fetchMultiOut'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/deleteall').delete(async (req, res) => {
  let tables = await db.query(`SHOW TABLES;`).catch(e => {
    res.status(500).send(e)
  })
  let result = []
  tables.forEach(async table => {
    let a_result = await db
      .query(`DELETE FROM ${table['Tables_in_secondtour']};`)
      .catch(e => {
        res.status(500).send(e)
      })
    result.push(a_result)
  })
  res.status(202).send(result)
})

/**
 * @swagger
 * /data/updatefilter/{table}:
 *    patch:
 *      tags:
 *          - Automated Data Operation
 *      description: Update all the rows of a table that match with your filter
 *      parameters:
 *          - in: path
 *            name: table
 *            type: string
 *            required: true
 *            description: The table you where you want to update rows
 *          - in: body
 *            name: User auth + Filter
 *            type: object
 *            schema:
 *              $ref: '#definitions/UserContentUpdate'
 *      responses:
 *          '202':
 *              description: Rows successfully updated
 *              schema:
 *                  $ref: '#definitions/returnId'
 *          '401':
 *              description: Your authentification identifiers are not correct
 */
router.route('/updatefilter/:table').patch(async (req, res) => {
  let table = req.params['table']
  let content = req.body['content']
  let content_condition = content['filter']
  let condition = ''
  Object.keys(content_condition).forEach((element, index) => {
    if (index != 0) condition += ' AND '
    if (
      content_condition[element] === 'null' ||
      !isNaN(content_condition[element]) ||
      content_condition[element] === 'true' ||
      content_condition[element] === 'false'
    )
      condition += element + ' = ' + content_condition[element]
    else condition += element + " = '" + content_condition[element] + "'"
  })
  let content_data = content['data']
  let data = ''
  Object.keys(content_data).forEach((element, index) => {
    if (content_data[element].toString().match(/... ... [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}/)) {
      content_data[element] =
        "STR_TO_DATE('" + content_data[element] + "', '%a %b %d %H:%i:%s %Y')"
        data += element + ' = ' + content_data[element]
    }else{
    if (
      content_data[element] === 'null' ||
      !isNaN(content_data[element]) ||
      content_data[element] === 'true' ||
      content_data[element] === 'false'
    )
      data += element + ' = ' + content_data[element]
    else data += element + ' = ' + "'" + content_data[element] + "'"
    }
    if (index != Object.keys(content_data).length - 1) data += ', '
  })
  let result = await db
    .query(`UPDATE ${table} SET ${data} WHERE ${condition};`)
    .catch(e => {
      res.status(500).send(e)
    })
  res.status(202).send(result)
})

module.exports = router
