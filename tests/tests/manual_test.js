require('dotenv').config()
const axios = require('axios')

function getContent (content = {}) {
  return {
    username: process.env.API_USERNAME,
    password: process.env.API_PASSWORD,
    content: content
  }
}

const URL = process.env.API_URL

for (let i = 0; i < 100; i++) {
  axios
    .post(URL + '/data/fetch/salle', getContent())
    .then(res => {
      console.log(`statusCode: ${res.status}`)
      // console.log(res)
    })
    .catch(error => {
      // console.error(error)
      console.error("Error")
    })

  // axios
  // .get(URL + '/version')
  // .then(res => {
  //   // console.log(`statusCode: ${res.status}`)
  //   // console.log(res)
  // })
  // .catch(error => {
  //   // console.error(error)
  //   console.error("Error")
  // })
}
