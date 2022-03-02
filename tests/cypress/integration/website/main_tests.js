/// <reference types="cypress" />
require('dotenv').config()


function goTo (path) {
  return cy.visit(Cypress.env('WEBSITE_URL') + path)
}

function getContent (content = {}) {
  return {
    username: Cypress.env('API_USERNAME'),
    password: Cypress.env('API_PASSWORD'),
    content: content
  }
}

describe('Testing the website UI',function () {
  beforeEach(function () {
  })

  it('Clean the db', () => {
    cy.request(
      'DELETE',
      Cypress.env('API_URL') + '/data/deleteall',
      getContent()
    ).then(response => {
      expect(response.status).to.eq(202)
    })
  })

  it('Insert the admin', () => {
    cy.request(
      'PUT',
      Cypress.env('API_URL') + '/data/insert/utilisateur',
      getContent({
        id_utilisateur: 'null',
        email: 'admin@ac-poitiers.fr',
        password: '$p5k2$3e8$AfpOzesj$.KoGR.raCRkA3gne.aZrF1bQobRfdSIH',
        admin: 'true',
        id_professeur: 'null'
      })
    ).then(response => {
      expect(response.status).to.eq(201)
    })
  })

  it('Get the empty index', () => {
    goTo('/')

    cy.get('table tbody tr').should('have.length', 0)
  })

  it('Try to access to a non authorized part', () => {
    goTo('/admin/')
    cy.url().should('match', /\/connexion/)
    goTo('/professeur/')
    cy.url().should('match', /\/connexion/)
  })

  it('Connect to the admin account with wrong identifiers', () => {
    goTo('/connexion')
    cy.get('#floatingInput').type(`unmail@gmail.com`)
    cy.get('#floatingPassword').type(`UnMotDePasse`)
    cy.get('form div button').click()

    cy.get('div.alert').should(list => {
      expect(list).to.have.length(1)
      expect(list.eq(0)).to.contain("Cet utilisateur n'existe pas")
    })
  })

  it('Connect to the admin account with correct identifiers',() => {
    goTo('/connexion')
    cy.get('#floatingInput').type(`admin@ac-poitiers.fr`)
    cy.get('#floatingPassword').type(`L0calAdmin`)
    cy.get('form div button').click()
    cy.url().should('match', /\/admin\/accueil/)
  })

  it('Try to generate an empty calendar',() => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/')
    cy.url().should('match', /\/admin\//)
    cy.get('button[data-bs-target="#generateCalendarModal"]').click({force: true})
    cy.get('#generateCalendarModal').should('be.visible')
    cy.get('[name="generate_button"]').click()
    cy.expectAlert('success', 'Calendrier généré avec succès')
  })

  it('Add a new salle', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/salles')
    cy.url().should('match', /\/admin\/salles/)
    cy.get('[data-bs-target="#addSalleModal"]').click({force: true})
    cy.get('#addSalleModal').should('be.visible')
    cy.get('#addSalleForm div input[name="numero"]').type("D001", { force: true }).should('contain.value', "D001")
    cy.get('button[form="addSalleForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'La salle a bien été crée')
    cy.get('table#calendar tbody tr td').eq(1).should("contain.text", "D001")
  })

  it('Add a new série technologique', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/series')
    cy.url().should('match', /\/admin\/serie/)
    cy.get('[data-bs-target="#addSerieModal"]').click({force: true})
    cy.get('#addSerieModal').should('be.visible')

    cy.get('#addSerieForm div select[name="serie"]').select('Technologique').should('contain.value', "Technologique")
    cy.get('#addSerieForm div input[name="specialite1"]').type('STI2D').should('contain.value', "STI2D")


    cy.get('button[form="addSerieForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'La série a bien été crée')
    cy.get('table#calendar tbody tr td').eq(1).should("contain.text", "Technologique")
    cy.get('table#calendar tbody tr td').eq(2).should("contain.text", "STI2D")
  })

  it('Add a new série générale', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/series')
    cy.url().should('match', /\/admin\/serie/)
    cy.get('[data-bs-target="#addSerieModal"]').click({force: true})
    cy.get('#addSerieModal').should('be.visible')

    cy.get('#addSerieForm div select[name="serie"]').select('Générale').should('contain.value', "Générale")
    cy.get('#addSerieForm div input[name="specialite1"]').type('Mathématiques').should('contain.value', "Mathématiques")
    cy.get('#addSerieForm div input[name="specialite2"]').type('SVT').should('contain.value', "SVT")


    cy.get('button[form="addSerieForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'La série a bien été crée')
    cy.get('table#calendar tbody tr td').eq(1).should("contain.text", "Générale")
    cy.get('table#calendar tbody tr td').eq(2).should("contain.text", "Mathématiques")
    cy.get('table#calendar tbody tr td').eq(3).should("contain.text", "SVT")
  })

  it('Verify that matieres are automatically generated', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/matieres')
    cy.url().should('match', /\/admin\/matieres/)
    
    let row = 0
    for(let i = 0; i < 2; i++){
      for(let y = 0; y < 2; y++){
        let serie = y == 0 ? "Technologique - STI2D" : "Générale - Mathématiques/SVT"
        let matiere = i == 0 ? "Français" : "Philosophie"
        cy.get(`#calendar > tbody > tr:nth-child(${(1+(row)*3)}) > td:nth-child(2)`).should("contain.text", matiere)
        cy.get(`#calendar > tbody > tr:nth-child(${(1+(row)*3)}) > td:nth-child(3)`).should("contain.text", serie)
        row++
      }
    }
  })

  it('Add a new matière', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/matieres')
    cy.url().should('match', /\/admin\/matieres/)
    cy.get('[data-bs-target="#addMatiereModal"]').click({force: true})
    cy.get('#addMatiereModal').should('be.visible')

    cy.get('#addMatiereForm div input[name="name"]').type('Mathématiques', {force: true}).should('contain.value', "Mathématiques")
    cy.get('#addMatiereForm div select[name="serie"]').select('Générale - Mathématiques/SVT').should('contain.text', "Générale - Mathématiques/SVT")
    cy.get('#addMatiereForm div input[name="temps_preparation"]').type('30').should('contain.value', "30")
    cy.get('#addMatiereForm div input[name="temps_preparation_tiers_temps"]').type('45').should('contain.value', "45")
    cy.get('#addMatiereForm div input[name="temps_passage"]').type('30').should('contain.value', "30")
    cy.get('#addMatiereForm div input[name="temps_passage_tiers_temps"]').type('45').should('contain.value', "45")


    cy.get('button[form="addMatiereForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'La matiere a bien été créée')

    cy.get('#calendar > tbody > tr > td:nth-child(2)').should("contain.text", "Mathématiques")
    cy.get('#calendar > tbody > tr > td:nth-child(3)').should("contain.text", "Générale - Mathématiques/SVT")
  })

  it('Add some new candidats', () => {
    cy.login("admin@ac-poitiers.fr", "L0calAdmin")
    goTo('/admin/candidats')
    cy.url().should('match', /\/admin\/candidats/)
    cy.get('[data-bs-target="#addCandidatModal"]').click({force: true})
    cy.get('#addCandidatModal').should('be.visible')

    cy.get('#addCandidatsForm div input[name="name"]').type('Pavet', {force: true}).should('contain.value', "Pavet")
    cy.get('#addCandidatsForm div input[name="surname"]').type('Bastien').should('contain.value', "Bastien")
    cy.get('#addCandidatsForm div select[name="serie"]').select('Générale - Mathématiques/SVT').should('contain.text', "Générale - Mathématiques/SVT")
    cy.get('#addCandidatsForm div select[name="matiere1"]').select('Mathématiques').should('contain.text', "Mathématiques")
    cy.get('#addCandidatsForm div select[name="matiere2"]').select('Français').should('contain.text', "Français")


    cy.get('button[form="addCandidatsForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'Les choix du candidat ont bien été crées')

    cy.get('#calendar > tbody > tr > td:nth-child(2)').should("contain.text", "Pavet")
    cy.get('#calendar > tbody > tr > td:nth-child(3)').should("contain.text", "Bastien")


    


    // Second candidat

    cy.get('[data-bs-target="#addCandidatModal"]').click({force: true})
    cy.get('#addCandidatModal').should('be.visible')

    cy.get('#addCandidatsForm div input[name="name"]').type('Galland', {force: true}).should('contain.value', "Galland")
    cy.get('#addCandidatsForm div input[name="surname"]').type('Jérémy').should('contain.value', "Jérémy")
    cy.get('#addCandidatsForm div select[name="serie"]').select('Technologique - STI2D').should('contain.text', "Technologique - STI2D")
    cy.get('#addCandidatsForm div select[name="matiere1"]').select('Philosophie').should('contain.text', "Philosophie")
    cy.get('#addCandidatsForm div select[name="matiere2"]').select('Français').should('contain.text', "Français")
    cy.get('#addCandidatsForm div select[name="absent"]').select('Oui').should('contain.text', "Oui")


    cy.get('button[form="addCandidatsForm"][name="submit_button"]').should("be.visible").click()
    cy.expectAlert('success', 'Les choix du candidat ont bien été crées')

    cy.get('#calendar > tbody > tr.table-danger > td:nth-child(2)').should("contain.text", "Galland")
    cy.get('#calendar > tbody > tr.table-danger > td:nth-child(3)').should("contain.text", "Jérémy")
  })
})
