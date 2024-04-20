import sqlite3

def inserisciViaggio(viaggio):
    success = False
    query = 'INSERT INTO viaggi (id_coordinatore, continente, nazione, data, num_giorni, aeroporto, prezzo, descrizione, img_viaggio, approvato, titolo) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (viaggio.get('id_coordinatore'), viaggio.get('continente'), viaggio.get('nazione'), viaggio.get('data'), viaggio.get('num_giorni'), viaggio.get('aeroporto'), viaggio.get('prezzo'), viaggio.get('descrizione'), viaggio.get('img_viaggio'), viaggio.get('approvato'), viaggio.get('titolo')))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success

def getIdViaggio(viaggio):
    query = 'SELECT id FROM viaggi WHERE continente = ? AND nazione = ? AND img_viaggio = ? AND id_coordinatore = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (viaggio.get('continente'), viaggio.get('nazione'), viaggio.get('img_viaggio'), viaggio.get('id_coordinatore')))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result  

def getViaggio(id_viaggio):
    query = 'SELECT * FROM viaggi WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def getViaggioAndPartecipazioni(id_viaggio):
    query = 'SELECT *, COUNT(partecipazioni_viaggi.id_utente) AS partecipanti FROM viaggi, utenti, partecipazioni_viaggi WHERE viaggi.id = ? AND utenti.id = viaggi.id_coordinatore AND viaggi.id = partecipazioni_viaggi.id_viaggio GROUP BY viaggi.id '
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def getViaggioEsistente(nazione, data):
    query = 'SELECT * FROM viaggi WHERE nazione = ? AND data = ? AND approvato = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (nazione, data, 1))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result  

def getViaggiInApprovazione():
    query = 'SELECT * FROM viaggi WHERE approvato = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (0,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 

def changeApprovazioneViaggio(id_viaggio):
    success = False
    query = 'UPDATE viaggi SET approvato = ? WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (1,id_viaggio))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success

def getIdCoordinatoreViaggio(id_viaggio):
    query = 'SELECT id_coordinatore FROM viaggi WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result 

def inserisciPartecipazioneViaggio(id_utente, id_viaggio):
    success = False
    query = 'INSERT INTO partecipazioni_viaggi (id_viaggio, id_utente) VALUES (?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (id_viaggio, id_utente))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success

def inserisciPartecipazioneViaggioConNota(id_utente, id_viaggio, nota):
    success = False
    query = 'INSERT INTO partecipazioni_viaggi (id_viaggio, id_utente, nota) VALUES (?,?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (id_viaggio, id_utente, nota))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def getViaggiCoordinatore(id_coordinatore):
    query = 'SELECT * FROM viaggi WHERE id_coordinatore = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_coordinatore,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 

def getViaggiCoordinatoreFiltro(id_coordinatore, filtro):
    query = 'SELECT * FROM viaggi WHERE id_coordinatore = ? AND approvato = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_coordinatore,filtro))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 

def getViaggiApprovati():
    query = 'SELECT * FROM viaggi WHERE approvato = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (1,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 

def getNumeroPartecipantiViaggio(id_viaggio):
    query = 'SELECT COUNT(id_utente) as partecipanti FROM partecipazioni_viaggi WHERE id_viaggio = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result 


def modificaImmagineViaggio(img_viaggio, id_viaggio):
    success = False
    query = 'UPDATE viaggi SET img_viaggio = ? WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (img_viaggio, id_viaggio))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def modificaInformazioniViaggio(nuovo_viaggio, id_viaggio):
    success = False
    query = 'UPDATE viaggi SET titolo = ?, data = ?, num_giorni = ?, aeroporto = ?, prezzo = ?, descrizione = ? WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (nuovo_viaggio.get('titolo'), nuovo_viaggio.get('data'), nuovo_viaggio.get('num_giorni'), nuovo_viaggio.get('aeroporto'), nuovo_viaggio.get('prezzo'), nuovo_viaggio.get('descrizione'), id_viaggio))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def getPartecipazioniViaggio(id_viaggio):
    query = 'SELECT * FROM partecipazioni_viaggi, utenti WHERE partecipazioni_viaggi.id_utente = utenti.id AND partecipazioni_viaggi.id_viaggio = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 


def getUtentiPartecipantiAlViaggio(id_viaggio):
    query = 'SELECT id_utente FROM partecipazioni_viaggi WHERE id_viaggio = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 


def getViaggiPrenotati(id_utente):
    query = 'SELECT * FROM partecipazioni_viaggi, viaggi WHERE viaggi.id = partecipazioni_viaggi.id_viaggio AND partecipazioni_viaggi.id_utente = ? AND viaggi.id_coordinatore != partecipazioni_viaggi.id_utente'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_utente,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 