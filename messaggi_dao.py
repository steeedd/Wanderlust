import sqlite3

def inserisciMessaggio(messaggio):
    success = False
    query = 'INSERT INTO messaggi (id_viaggio, id_utente, txtMessaggio, data) VALUES (?,?,?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (messaggio.get('id_viaggio'), messaggio.get('id_utente'), messaggio.get('testo'), messaggio.get('data')))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def getMessaggiViaggio(id_viaggio):
    query = 'SELECT * FROM messaggi, utenti WHERE messaggi.id_viaggio = ? AND messaggi.id_utente = utenti.id ORDER BY messaggi.data ASC'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id_viaggio,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result 