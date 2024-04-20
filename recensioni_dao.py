import sqlite3

def getRecensioneViaggioUtente(id_viaggio, id_utente):
    query = 'SELECT * FROM recensioni WHERE id_viaggio = ? AND id_utente = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,id_utente))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result 

def inserisciRecensione(recensione):
    success = False
    query = 'INSERT INTO recensioni (id_utente, id_viaggio, testo, valutazione_avventura, valutazione_divertimento, valutazione_relax) VALUES (?,?,?,?,?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (recensione.get('id_utente'), recensione.get('id_viaggio'), recensione.get('testo'), recensione.get('valutazione_avventura'), recensione.get('valutazione_divertimento'), recensione.get('valutazione_relax')))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def getRecensioniViaggio(nazione):
    query = 'SELECT * FROM recensioni, viaggi, utenti WHERE nazione = ? AND viaggi.id = recensioni.id_viaggio AND recensioni.id_utente = utenti.id'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (nazione,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result