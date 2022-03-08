const express = require('express')
const app = express()
const swaggerJsDoc = require('swagger-jsdoc')
const swaggerUi = require('swagger-ui-express')
require('dotenv').config({path:".env_dev"})
const fs = require('fs')

// Database
var db = require('./database/config')

// Custom logs
app.use(function (req, res, next) {
  res.on('finish', function () {
    let data =
      Date.now() +
      '\nFROM:\n\tIP :' +
      req.ip +
      ' : \nREQUEST :\n\tMethod : ' +
      req.method +
      '\n\tUrl : ' +
      req.url +
      '\n\tBody : ' +
      (JSON.stringify(req.body) || "No body")
    fs.appendFile('./logs/log_info.log', data, err => {
      // In case of a error throw err.
      if (err) throw err
    })
    console.log(req.method, req.url, res.statusCode)
  })
  next()
})

const port = process.env.PORT || 5000

// Extended: https://swagger.io/specification/#infoObject
const swaggerOptions = {
  swaggerDefinition: {
    info: {
      version: '1.0.0',
      title: 'Secondtour API',
      description:
        'This API make the link between the secondtour website and database',
      contact: {
        name: 'IUT Larochelle',
        url: 'https://www.iut-larochelle.fr/'
      },
      externalDocs: {
        description: 'Github documentation',
        url:
          'https://forge.iut-larochelle.fr/lhuort/pts2021_sujet14/-/wikis/Pr%C3%A9sentation-du-projet'
      },
      tags: [
        {
          name: 'Automated Data Operation',
          description:
            'This routes can operate on evey single table of the database so errors may occurs'
        }
      ]
    },
    definitions: {
      User: {
        type: 'object',
        required: ['username', 'password'],
        properties: {
          username: {
            type: 'string',
            description: 'Username of the user',
            example: 'Admin'
          },
          password: {
            type: 'string',
            description: 'Password of the user',
            example: 'Password123'
          }
        }
      },
      UserContentTableName: {
        type: 'object',
        required: ['username', 'password', 'content'],
        properties: {
          username: {
            type: 'string',
            description: 'Username of the user',
            example: 'Admin'
          },
          password: {
            type: 'string',
            description: 'Password of the user',
            example: 'Password123'
          },
          content: {
            type: 'array',
            description: 'Name of all the table you want to retreive',
            items: {
              type: 'string',
              example: 'salle'
            },
            example: ['salle', 'creneau', 'utilisateur']
          }
        }
      },
      UserContentTableDescription: {
        type: 'object',
        required: ['username', 'password', 'content'],
        properties: {
          username: {
            type: 'string',
            description: 'Username of the user',
            example: 'Admin'
          },
          password: {
            type: 'string',
            description: 'Password of the user',
            example: 'Password123'
          },
          content: {
            type: 'object',
            description: 'All filter you want to put',
            example: {
              numero: 'D002'
            }
          }
        }
      },
      UserContentTableDescriptionFull: {
        type: 'object',
        required: ['username', 'password', 'content'],
        properties: {
          username: {
            type: 'string',
            description: 'Username of the user',
            example: 'Admin'
          },
          password: {
            type: 'string',
            description: 'Password of the user',
            example: 'Password123'
          },
          content: {
            type: 'object',
            description: 'All the necessary element you need to insert a row',
            example: {
              id_salle: 'null',
              numero: 'D002'
            }
          }
        }
      },
      UserContentUpdate: {
        type: 'object',
        required: ['username', 'password', 'content'],
        properties: {
          username: {
            type: 'string',
            description: 'Username of the user',
            example: 'Admin'
          },
          password: {
            type: 'string',
            description: 'Password of the user',
            example: 'Password123'
          },
          content: {
            type: 'object',
            description:
              'The filter and the data to replace in the rows selected',
            properties: {
              filer: {
                type: 'object',
                example: {
                  id_salle: '1'
                }
              },
              data: {
                type: 'object',
                example: {
                  numero: 'D002'
                }
              }
            },
            example: {
              filter: {
                id_salle: '1'
              },
              data: {
                numero: 'D002'
              }
            }
          }
        }
      },
      fetchOut: {
        type: 'array',
        items: {
          type: 'object',
          example: {
            id_salle: 2,
            numero: 'D002'
          }
        },
        example: [
          {
            id_salle: 1,
            numero: 'D001'
          },
          {
            id_salle: 2,
            numero: 'D002'
          }
        ]
      },
      fetchFilterOut: {
        type: 'array',
        items: {
          type: 'object',
          example: {
            id_salle: 2,
            numero: 'D002'
          }
        },
        example: [
          {
            id_salle: 2,
            numero: 'D002'
          }
        ]
      },
      fetchMultiOut: {
        type: 'array',
        items: {
          type: 'array',
          items: {
            type: 'object',
            example: {
              id_salle: 2,
              numero: 'D002'
            }
          },
          example: [
            {
              id_salle: 2,
              numero: 'D002'
            }
          ]
        },
        example: [
          [
            {
              id_salle: 1,
              numero: 'D001'
            },
            {
              id_salle: 2,
              numero: 'D002'
            }
          ],
          [
            {
              id_liste_matiere: 1,
              id_professeur: 1,
              id_matiere: 1
            }
          ]
        ]
      },
      returnId:{
        type: 'int',
        example: 1
      }
    }
  },
  apis: ['app.js', 'routes/*']
}

const swaggerDocs = swaggerJsDoc(swaggerOptions)
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs))

app.listen(port, () => {
  console.log(`Server listening on port ${port}`)
})

app.use(express.json())

const main_routes = require('./routes/main_routes')
app.use('/', main_routes)
const advanced_routes = require('./routes/advanced_routes')
app.use('/data', advanced_routes)
