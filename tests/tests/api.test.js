require('dotenv').config()
const supertest = require('supertest')
jest.useFakeTimers()

function getContent (content = {}) {
  return {
    username: process.env.API_USERNAME,
    password: process.env.API_PASSWORD,
    content: content
  }
}

expect.extend({
  toBeBetween (received, floor, ceiling) {
    const pass = received >= floor && received < ceiling
    if (!pass) {
      return {
        message: () =>
          `expected ${received} to be between range ${floor} - ${ceiling}`,
        pass: false
      }
    } else {
      return {
        message: () =>
          `expected ${received} not to be between range ${floor} - ${ceiling}`,
        pass: true
      }
    }
  }
})

describe('API', () => {
  let request

  beforeEach(() => {
    request = supertest(process.env.API_URL)
  })

  it('Clean all the tables content', async () => {
    const res = await request.delete('/data/deleteall').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
  })

  it('Return the version of the api', async () => {
    const res = await request.get('/version')
    expect(res.statusCode).toBeBetween(200, 302)
  })

  it('Return the doc of the api', async () => {
    const res = await request.get('/docs')
    expect(res.statusCode).toBeBetween(200, 302)
  })

  it('Return all the content of a table (testing for all tables)', async () => {
    let allTables = [
      'candidat',
      'choix_matiere',
      'creneau',
      'horaire',
      'liste_matiere',
      'matiere',
      'professeur',
      'salle',
      'serie',
      'token',
      'utilisateur'
    ]
    for (let i = 0; i < allTables.length; i++) {
      let tableName = allTables[i]
      const res = await request
        .post(`/data/fetch/${tableName}`)
        .send(getContent())
        .catch(err => {
          console.error(err)
        })
      expect(res.statusCode).toBeBetween(200, 300)
    }
  })

  it('Clean all the tables content', async () => {
    const res = await request.delete('/data/deleteall').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
  })

  it('Insert a row', async () => {
    let res = await request
      .put('/data/insert/salle')
      .send(getContent({ id_salle: 'null', numero: 'D001' }))
    expect(res.statusCode).toBeBetween(200, 300)

    res = await request
      .post('/data/fetch/salle')
      .send(getContent())
      .catch(err => {
        console.error(err)
      })
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      {
        numero: 'D001'
      }
    ])
  })

  it('Perform a fetch filtered', async () => {
    let res = await request
      .post('/data/fetchfilter/salle')
      .send(getContent({ numero: 'D001' }))
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      {
        numero: 'D001'
      }
    ])

    res = await request
      .post('/data/fetchfilter/salle')
      .send(getContent({ numero: 'D002' }))
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([])
  })

  it('Perform a multi fetch', async () => {
    let res = await request.put('/data/insert/serie').send(
      getContent({
        id_serie: 'null',
        nom: 'Generale',
        specialite1: 'Mathématiques',
        specialite2: 'SVT'
      })
    )
    expect(res.statusCode).toBeBetween(200, 300)

    res = await request
      .post('/data/fetchmulti')
      .send(getContent(['salle', 'serie']))
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      [{ numero: 'D001' }],
      [
        {
          nom: 'Generale',
          specialite1: 'Mathématiques',
          specialite2: 'SVT'
        }
      ]
    ])
  })

  it('Update a row', async () => {
    let res = await request.post('/data/fetch/salle').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      {
        numero: 'D001'
      }
    ])
    let salle_id = res.body[0]['id_salle']

    res = await request.patch('/data/updatefilter/salle').send(
      getContent({
        filter: { id_salle: salle_id.toString() },
        data: { numero: 'D002' }
      })
    )
    expect(res.statusCode).toBeBetween(200, 300)

    res = await request.post('/data/fetch/salle').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      {
        numero: 'D002'
      }
    ])
  })

  it('Delete all rows of a table', async () => {
    let res = await request.delete('/data/delete/salle').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    res = await request.post('/data/fetch/salle').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([])
  })

  it('Delete all rows filtered', async () => {
    let res = await request.delete('/data/deletefilter/serie').send(
      getContent({
        nom: 'ThisNameDoesntExist'
      })
    )
    expect(res.statusCode).toBeBetween(200, 300)

    res = await request.post('/data/fetch/serie').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([
      {
        nom: 'Generale',
        specialite1: 'Mathématiques',
        specialite2: 'SVT'
      }
    ])

    res = await request.delete('/data/deletefilter/serie').send(
      getContent({
        nom: 'Generale'
      })
    )
    expect(res.statusCode).toBeBetween(200, 300)

    res = await request.post('/data/fetch/serie').send(getContent())
    expect(res.statusCode).toBeBetween(200, 300)
    expect(res.body).toMatchObject([])
  })

  it('Insert the admin user', async () => {
    // By precaution
    await request.delete('/data/deletefilter/utilisateur').send(
      getContent({
        email: 'admin@ac-poitiers.fr'
      })
    )

    const res = await request
      .put('/data/insert/utilisateur')
      .send(
        getContent({
          id_utilisateur: 'null',
          email: 'admin@ac-poitiers.fr',
          password: '$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH',
          admin: 'true',
          id_professeur: 'null'
        })
      )
    expect(res.statusCode).toBeBetween(200, 300)
  })
})
