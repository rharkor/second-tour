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

module.exports = router