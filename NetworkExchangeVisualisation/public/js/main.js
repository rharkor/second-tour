let items = []
let acutalItems = []
let cy

// When the doc is ready
$(document).ready(function () {
  // Start the readFile interval
  setInterval(readFile, 75)

  // Create the cy object
  cy = cytoscape({
    container: document.getElementById('cy'),
    boxSelectionEnabled: false,
    autounselectify: true,
    style: cytoscape
      .stylesheet()
      .selector('node')
      .style({
        content: 'data(name)',
        color: '#fff',
        width: 'data(size)',
        height: 'data(size)',
        "font-size": 'data(fsize)',
      })
      .selector('edge')
      .style({
        'curve-style': 'bezier',
        width: 4,
        'line-color': '#888'
      })
      .selector('.highlighted')
      .style({
        'background-color': 'yellow',
        'line-color': 'yellow'
      })
  })
})

// Create a function that read the file data.json each 200ms
function readFile () {
  // Get the content of the file public/data/data.json
  fetch('/data')
    .then(response => response.json())
    .then(data => {
      items = data
      renderItems()
    })
    .catch(error => {})
}

function renderItems () {
  items.forEach(item => {
    // test if item is already in acutalItems
    if (acutalItems.filter(i => i.id === item.id).length === 0) {
      try {
        if (item.type === 'node') {
          cy.add({
            group: 'nodes',
            data: item.data,
            position: item.position
          })
        } else if (item.type === 'edge') {
          cy.add({
            group: 'edges',
            data: item.data
          })
        } else if (item.type === 'trigger') {
          animateEdge(item.data.target)
        }
        acutalItems.push(item)
      } catch (e) {
        // console.log(e)
      }
    }
  })
}

function animateEdge (target) {
  let bfs = cy.getElementById(target)
  bfs.addClass('highlighted')
  bfs.lastUpdate = Date.now()
  checkLastUpdate(bfs)
}

function checkLastUpdate (element) {
  setTimeout(() => {
    if (Date.now() - element.lastUpdate >= 1000) {
      element.removeClass('highlighted')
    }
  }, 1000)
}
