# APPLICAZIONE WEB - WANDERLUST

Wanderlust è un'applicazione web progettata per facilitare la gestione di viaggi di gruppo, offrendo un'organizzazione intuitiva per soddisfare le esigenze di tre categorie di utenti distinti presenti sulla piattaforma.

L'amministratore, il creatore del sito, viene automaticamente inserito nel database durante la creazione dell'applicazione e non richiede una registrazione formale. Le sue prerogative comprendono la visualizzazione degli utenti iscritti e la gestione di tali utenti. In particolare, ha la facoltà di promuovere un utente al ruolo di "coordinatore" e, altresì, di espellere un utente mediante il blocco e la cancellazione del suo account dalla piattaforma.

Gli utenti registrati possono esplorare i vari viaggi proposti sul sito e, se interessati, procedere con la prenotazione. Tuttavia, non hanno il diritto di proporre nuovi viaggi, prerogativa riservata ai coordinatori. La designazione a coordinatore avviene esclusivamente per decisione dell'amministratore.

I coordinatori, oltre alla possibilità di partecipare ai viaggi proposti, hanno il privilegio di creare nuove proposte. Ogni viaggio è caratterizzato da una destinazione, un riassunto delle attività pianificate, una durata, una data di partenza, un aeroporto di partenza e il numero attuale di partecipanti. Al momento della creazione di un viaggio, il coordinatore viene automaticamente incluso tra i partecipanti. I coordinatori possono anche modificare le informazioni sul viaggio, ad eccezione della destinazione, che rimane fissa. Un viaggio, dopo essere stato proposto dal coordinatore, dovrà essere approvato in modo DEFINITIVO dall'amministratore per comparire nella homepage del sito affinchè altri utenti possano parteciparvi.

Gli utenti, sulla homepage del sito, trovano l'elenco completo dei viaggi disponibili e possono aderire a quelli di loro interesse inserendo i dati necessari per il pagamento. Solo i viaggi con una data di partenza successiva a quella corrente sono visibili sulla homepage (i viaggi passati non vengono mostrati). Cliccando su un viaggio, gli utenti vengono reindirizzati alla pagina "ufficiale" dedicata al viaggio, con maggiori informazioni. Nella homepage, è possibile filtrare i viaggi per continente di destinazione, visualizzarli in ordine crescente di prezzo o decrescente di partecipanti attuali.

Ogni utente ha una pagina profilo con sezioni dedicate alle informazioni personali e ai viaggi. La sezione viaggi è suddivisa tra viaggi passati e futuri. La pagina profilo è personale, consentendo a ogni utente di visualizzare solo la propria pagina, senza accesso alle pagine degli altri utenti.

I viaggi verso una stessa destinazione non sono unici; possono esserci molteplici partenze per lo stesso paese, con l'unica restrizione di evitare partenze nello stesso giorno per lo stesso luogo. Gli utenti che partecipano a un viaggio hanno la possibilità, in una data successiva, di lasciare una recensione. La recensione non è visibile solo nella pagina del viaggio passato, ma anche nelle pagine di tutti i viaggi con la stessa destinazione. Inoltre, l'utente può modificarla in qualsiasi momento.

# PAGINE WEB
* Home:
    - elenco dei viaggi disponibili
    - filtro di ricerca per nazione
    - filtro dei viaggi per continente
    - filtro per visualizzare i viaggi in ordine crescente di prezzo
    - filtro per visualizzare i viaggi in ordine decrescente di partecipanti attuali

* Homepage del viaggio:
    - descrizione completa del viaggio con tutte le informazioni complete
    - carousel delle immagini del viaggio effettuato
    - elenco delle recensioni, con anche la valutazione media (utilizzare le star)
    - possibilità per un utente che non partecipa al viaggio di prenotarsi, tramite un bottone, che gli permette di inserire i dati per il pagamento
    - possibilità, solamente per il coordinatore che ha proposto il viaggio, di modificare cliccando su un bottone visibile solo a lui le informazioni sul viaggio

* Pagina profilo utente:
    - sezione dedicata alle informazioni personali
    - sezione dedicata ai viaggi prenotati, divisa tra i viaggi passati e quelli futuri

* Pagina profilo coordinatore:
    - sezione dedicata alle informazioni personali
    - sezione dedicata ai viaggi prenotati, divisa tra i viaggi passati e quelli futuri
    - sezione dedicata ai viaggi proposti

* Pagina profilo amministratore:
    - sezione dedicata alle informazioni personali
    - sezione dedicata ai viaggi prenotati, divisa tra i viaggi passati e quelli futuri
    - sezione dedicata ai viaggi proposti
    - possibilità di accedere a una sezione in cui sono visibili tutti gli utenti del sito, con la possibilità di promuovere un utente a coordinatore oppure bannarlo.

* Pagina Login - Signup:
    - form per l'inserimento dei dati

* Pagina ERROR 404/405
