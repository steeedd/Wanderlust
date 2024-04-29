// Funzione che serve per ordinare gli annunci in ordine crescente di prezzo
function orderByPrice() {
    const articles = document.querySelectorAll('.image-container');
    const sortedArticles = Array.from(articles).sort((a, b) => { //.querySelectorAll() restituisci una nodeList. La nodeList non ha il metodo .sort(), e quindi con Array.from(articles) trasformo la nodeList in un array JS.
        const priceA = parseFloat(a.dataset.prezzo);
        const priceB = parseFloat(b.dataset.prezzo);
        return priceA - priceB;
    });
    const section = document.querySelector('#sectionViaggi');
    section.innerHTML = '';
    sortedArticles.forEach(article => {
        section.appendChild(article);
    });

    document.getElementById('sectionPrezzo').classList.add('selected');
    document.getElementById('sectionPartecipanti').classList.remove('selected');
}

// Funzione che serve per ordinare gli annunci in ordine decrescente di numero di partecipanti
function orderByParticipants() {
    const articles = document.querySelectorAll('.image-container');
    const sortedArticles = Array.from(articles).sort((a, b) => {
        const participantsA = parseInt(a.dataset.partecipanti);
        const participantsB = parseInt(b.dataset.partecipanti);
        return participantsB - participantsA;
    });
    const section = document.querySelector('#sectionViaggi');
    section.innerHTML = '';
    sortedArticles.forEach(article => {
        section.appendChild(article);
    });

    document.getElementById('sectionPartecipanti').classList.add('selected');
    document.getElementById('sectionPrezzo').classList.remove('selected');
}


document.getElementById('sectionPrezzo').addEventListener('click', orderByPrice);
document.getElementById('sectionPartecipanti').addEventListener('click', orderByParticipants);




// Filtro per continente
document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', function() {
        const filter = this.textContent.trim();
        const viaggi = document.querySelectorAll('.image-container'); // Selezioniamo tutti gli articoli dei viaggi

        if (filter === 'Tutti') { // Se l'opzione "Tutti" è selezionata, mostriamo tutti i viaggi
            for (let viaggio of viaggi)
            viaggio.classList.remove('hide');
            document.getElementById('continentAnchor').textContent = "Tutti"
        } 
        else { // Altrimenti, filtriamo i viaggi in base al continente selezionato
        for (let viaggio of viaggi) {
          const continenteViaggio = viaggio.getAttribute('data-continente'); // Otteniamo il continente del viaggio
          if (continenteViaggio === filter) {
            viaggio.classList.remove('hide');
          } else {
            viaggio.classList.add('hide');
          }
          document.getElementById('continentAnchor').textContent = filter
        }

      }
      controllaViaggiPresenti()
    });
    
});



// Filtro per nazione
document.getElementById('nationFilter').addEventListener('keyup', e => { // keyup è un evento che viene attivato quando un tasto della tastiera viene rilasciato mentre un elemento DOM ha il focus, in questo caso l'input con ID nationFilter
    e.preventDefault();
  
    let filter = document.getElementById('nationFilter').value.toLowerCase();
    const viaggi = document.querySelectorAll('.image-container');
  
    for (let viaggio of viaggi) {
        nazione = viaggio.getAttribute('data-nazione').toLowerCase()
      if (nazione.includes(filter)) {
        viaggio.classList.remove('nascondi');
      }
      else
        viaggio.classList.add('nascondi');
    }
    controllaViaggiPresenti()
});



function controllaViaggiPresenti() {
    const viaggi = document.querySelectorAll('.image-container:not(.hide):not(.nascondi)');
    const messaggioAvviso = document.getElementById('messaggioAvviso');

    if (viaggi.length === 0) {
        messaggioAvviso.classList.remove('hide');
    } else {
        messaggioAvviso.classList.add('hide');
    }
}
