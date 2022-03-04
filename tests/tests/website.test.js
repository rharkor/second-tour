require('dotenv').config()
const supertest = require('supertest')
const session = require('supertest-session')
jest.useFakeTimers()

function sleep(time){
  return new Promise(r => setTimeout(r, time))
}

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
  },
  toHaveFlashError (received) {
    const regex = /<div role="alert" class="alert alert-danger  alert-dismissible fade show">\s*[\w\s',)(]*\s*<button type="button" data-bs-dismiss="alert" aria-label="Close" class="btn-close"><\/button><\/div>/
    const pass = received.match(regex)
    if (!pass) {
      return {
        message: () => `expected to have some errors`,
        pass: true
      }
    } else {
      return {
        message: () => `expected to not conaint any error messages`,
        pass: false
      }
    }
  }
})

describe('WEBSITE RESPONSE', () => {
  let request, requestApi
  let authenticatedSession = session(process.env.WEBSITE_URL)

  beforeEach(() => {
    request = supertest(process.env.WEBSITE_URL)
    requestApi = supertest(process.env.API_URL)
  })



  it('Return the index of the website', async () => {
    const res = await request.get('/')
    expect(res.statusCode).toBeBetween(200, 300)
  })

  it('Return the login page of the website', async () => {
    const res = await request.get('/connexion')
    expect(res.statusCode).toBeBetween(200, 300)
  })

  it('Test the non access to the admin part when no auth is given', async () => {
    let res = await request.get('/admin/')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/salles')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/series')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/matieres')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/candidats')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/professeurs')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/creneau')
    expect(res.statusCode).toEqual(302)

    res = await request.get('/admin/comptes')
    expect(res.statusCode).toEqual(302)
  })

  it('Test the non access to the professeur part when no auth is given', async () => {
    const res = await request.get('/professeur/')
    expect(res.statusCode).toEqual(302)
  })

  it('Try to connect with incorrect auth', async () => {
    const res = await request
      .post('/connexion')
      .send('email=unAdmin%40ac-poitiers.fr&password=unMotdepass')
    expect(res.statusCode).toEqual(401)
  })

  it('Try to connect with correct auth', async () => {
    let res = await authenticatedSession
      .post('/connexion')
      .send('email=admin%40ac-poitiers.fr&password=L0calAdmin')
    if (res.statusCode != 302){
      await requestApi
      .put('/data/insert/utilisateur')
      .send(getContent({ id_utilisateur: 'null', email: 'admin@ac-poitiers.fr', password: '$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH', admin: 'true', id_professeur: 'null'}))

      res = await authenticatedSession
      .post('/connexion')
      .send('email=admin%40ac-poitiers.fr&password=L0calAdmin')
    }
    expect(res.statusCode).toEqual(302)
  })

  it('Try to access to the admin section (session)', async () => {
    const res = await authenticatedSession.get('/admin/')
    expect(res.statusCode).toEqual(200)
  })
})
