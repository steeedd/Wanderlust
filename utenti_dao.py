import sqlite3

def getUtenteByID(id):
    query = 'SELECT * FROM utenti WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result 

def getIdUtenteByEmail(email):
    query = 'SELECT id FROM utenti WHERE email = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def getUtenteByEmail(email):
    query = 'SELECT * FROM utenti WHERE email = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result  

def inserisciUtente(user):
    success = False
    query = 'INSERT INTO utenti (nome, cognome, email, password, tipologia, img_profilo, banned) VALUES (?,?,?,?,?,?,?)'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (user.get('nome'), user.get('cognome'), user.get('email'), user.get('password'), user.get('tipologia'), user.get('img_profilo'), 0))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success

def getUtenti():
    query = 'SELECT * FROM utenti ORDER BY banned ASC, email ASC'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result  


def modificaTipologiaUtente(id_utente):
    success = False
    query = 'UPDATE utenti SET tipologia = ? WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, ('coordinatore',id_utente))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success


def banUtente(id_utente):
    success = False
    query = 'UPDATE utenti SET banned = ? WHERE id = ?'
    connection = sqlite3.connect('db/wanderlust.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    try:
        cursor.execute(query, (1, id_utente))
        connection.commit()
        success = True

    except Exception as e:
        print('Error: ' + str(e))
        connection.rollback()

    cursor.close
    connection.close

    return success
