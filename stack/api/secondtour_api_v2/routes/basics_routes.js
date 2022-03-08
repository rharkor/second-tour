const express = require('express')
const router = express.Router()

 router.route('/wow').post(async (req, res) => {
  //  console.log("here")
  // let table = req.params['table']
  // let result = await db.query(`SELECT * FROM ${table};`).catch(e => {
  //   res.status(500).send(e)
  // })
  res.send("here")
})

module.exports = router
