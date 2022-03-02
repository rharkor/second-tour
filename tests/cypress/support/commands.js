// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('login', (email, password) => {
  // cy.task('log', 'HEREEEE')
  cy.request({
    method: 'POST',
    url: '/connexion',
    form: true,
    body: { email: email, password: password }
  }).then(response => {
    let session_cookies = response.headers['set-cookie'][0]
      .replace('session=', '')
      .split(';')

    cy.wrap(session_cookies).as('session_cookies')

    cy.setCookie('session', session_cookies[0], session_cookies)
    cy.getCookie('session').should('have.property', 'value')
  })
})

Cypress.Commands.add('expectAlert', (type, message) => {
  cy.get('div.alert.alert-' + type).each(($el) => {
      expect($el).to.contain(message)
  })
})
