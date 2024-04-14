# pip install flask
from flask import Flask, render_template, request, url_for, redirect, flash
# pip install flask_login
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# pip install werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
# pip install Pillow
from PIL import Image
from datetime import datetime, timedelta
import os

from models import User
import utenti_dao, viaggi_dao


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkdwIO3KSoso2oi1393JDI2k2k1'

login_manager = LoginManager()
login_manager.init_app(app)

PROFILE_IMG_HEIGHT = 160
JOURNEY_IMG_HEIGHT = 390


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    viaggi_approvati = viaggi_dao.getViaggiApprovati()
    oggi = datetime.now().strftime('%Y-%m-%d')

    return render_template('home.html', viaggi_approvati=viaggi_approvati, oggi=oggi)

@app.route('/registrazione')
def iscriviti():
    return render_template('signup.html')


@app.route('/signup', methods = ['POST'])
def signup():
    user_signup = request.form.to_dict()

    if user_signup.get('nome') == '':
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('iscriviti'))
    
    if user_signup.get('cognome') == '':
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('iscriviti'))
    
    if user_signup.get('email') == '':
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('iscriviti'))
    
    if user_signup.get('password') == '':
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('iscriviti'))
    
    if len(user_signup.get('nome')) < 2:
        flash('Il nome inserito non è valido')
        return redirect(url_for('iscriviti'))
    
    if len(user_signup.get('cognome')) < 2:
        flash('Il cognome inserito non è valido')
        return redirect(url_for('iscriviti'))
    
    if '@' not in user_signup.get('email') or '.' not in user_signup.get('email'):
        flash('La mail inserita non esiste! La preghiamo di inserire un indirizzo mail valido', 'danger')
        return redirect(url_for('iscriviti'))
    
    if '1' not in user_signup.get('password') and '2' not in user_signup.get('password') and '3' not in user_signup.get('password') and '4' not in user_signup.get('password') and '5' not in user_signup.get('password') and '6' not in user_signup.get('password') and '7' not in user_signup.get('password') and '8' not in user_signup.get('password') and '9' not in user_signup.get('password') and '0' not in user_signup.get('password'):
        flash('La password deve contentere un numero!', 'danger')
        return redirect(url_for('iscriviti'))
    
    verifica_email = utenti_dao.getIdUtenteByEmail(user_signup.get('email'))
    if verifica_email:
        flash('Questa email risulta già registrata!', 'warning')
        return redirect(url_for('iscriviti'))
    
    user_signup['password'] = generate_password_hash(user_signup.get('password'))

    immagine = request.files.get('immagine_profilo')
    if immagine: 
        img = Image.open(immagine)

        width, height = img.size
        new_width = PROFILE_IMG_HEIGHT * width / height

        size = new_width, PROFILE_IMG_HEIGHT
        img.thumbnail(size, Image.Resampling.LANCZOS)

        left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
        top = 0
        right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
        bottom = PROFILE_IMG_HEIGHT

        img = img.crop((left, top, right, bottom))

        ext = immagine.filename.split('.')[-1]

        img.save('static/utenti/' + user_signup.get('email').lower() + '.' + ext)

        img_profilo = user_signup.get('email').lower() + '.' + ext
        user_signup['img_profilo'] = img_profilo

    else:
        user_signup['img_profilo'] = 'user.jpg'

    success = utenti_dao.inserisciUtente(user_signup)
    if success: 
        flash('Registrazione avvenuta con successo!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Qualcosa è andato storto...', 'warning')
        return redirect(url_for('iscriviti'))


@app.route ('/accedi_form')
def login_page():
    return render_template('login.html')

@app.route('/login' , methods = ['POST'])
def login():
    user_logged = request.form.to_dict()
    utente = utenti_dao.getUtenteByEmail(user_logged.get('email'))

    if utente['banned'] == 1:
        flash(f'Ciao {utente["nome"]}. Siamo spiacenti di informarti che il tuo account è stato bannato dal nostro sito. Questa decisione è stata presa a seguito di una violazione dei nostri Termini di Servizio o delle nostre Linee Guida della Comunità. Se credi che questo ban sia stato un errore o desideri chiarimenti sulla sua motivazione, ti preghiamo di contattare il nostro team di supporto all\'indirizzo mail info@wanderlust.com.', 'warning')
        return redirect(url_for('index'))
    
    if utente and check_password_hash(utente['password'], user_logged.get('password')):
        flash('Login effettuato con successo!', 'success')
        new = User(id=utente['id'], nome = utente['nome'], cognome = utente['cognome'], email = utente['email'], password = utente['password'], tipologia = utente['tipologia'], img_profilo = utente['img_profilo'])
        login_user(new)
        return redirect(url_for('index'))

    else:
        flash('La mail e/o la password inserita non è corretta', 'danger')
        return redirect(url_for('login_page'))
    

@app.route('/profilo', methods = ['POST', 'GET'])
@login_required
def area_personale():
    un_mese_dopo = (datetime.now() + timedelta(weeks=4)).strftime('%Y-%m-%d')
    aeroporti_italiani = [
    "Roma-Fiumicino - FCO", "Milano-Malpensa - MXP", "Milano-Linate - LIN", "Venezia Marco Polo - VCE", "Napoli-Capodichino - NAP", "Firenze-Peretola - FLR", "Bologna-Guglielmo Marconi - BLQ", "Catania-Fontanarossa - CTA", "Palermo-Punta Raisi - PMO", "Bergamo-Orio al Serio - BGY", "Pisa Galileo Galilei - PSA", "Verona-Villafranca - VRN", "Torino-Caselle - TRN", "Bari-Palese - BRI", "Cagliari-Elmas - CAG", "Trapani-Birgi - TPS", "Brindisi-Casale - BDS", "Genova-Cristoforo Colombo - GOA", "Perugia-Sant'Egidio - PEG", "Ancona-Falconara - AOI"
]
    filtroApprovazione = request.form.get('filtroApprovazione', 'all')
    if filtroApprovazione == 'all':
        viaggi_coordinatore = viaggi_dao.getViaggiCoordinatore(current_user.id)
    else:
        filtro = int(filtroApprovazione)
        viaggi_coordinatore = viaggi_dao.getViaggiCoordinatoreFiltro(current_user.id, filtro)


    return render_template('profilo.html', un_mese_dopo=un_mese_dopo, aeroporti_italiani=aeroporti_italiani, viaggi_coordinatore = viaggi_coordinatore, filtroApprovazione=filtroApprovazione)

@app.route('/viaggio/<int:id_viaggio>')
def pagina_viaggio(id_viaggio):
    viaggio = viaggi_dao.getViaggioAndPartecipazioni(id_viaggio)
    aeroporti_italiani = [
    "Roma-Fiumicino - FCO", "Milano-Malpensa - MXP", "Milano-Linate - LIN", "Venezia Marco Polo - VCE", "Napoli-Capodichino - NAP", "Firenze-Peretola - FLR", "Bologna-Guglielmo Marconi - BLQ", "Catania-Fontanarossa - CTA", "Palermo-Punta Raisi - PMO", "Bergamo-Orio al Serio - BGY", "Pisa Galileo Galilei - PSA", "Verona-Villafranca - VRN", "Torino-Caselle - TRN", "Bari-Palese - BRI", "Cagliari-Elmas - CAG", "Trapani-Birgi - TPS", "Brindisi-Casale - BDS", "Genova-Cristoforo Colombo - GOA", "Perugia-Sant'Egidio - PEG", "Ancona-Falconara - AOI"
]

    return render_template('viaggio.html', viaggio = viaggio, aeroporti_italiani=aeroporti_italiani)

@app.route('/<int:id_utente>/nuovo_viaggio', methods=['POST'])
@login_required
def nuovo_viaggio(id_utente):
    if id_utente != current_user.id:
        return render_template('405.html'), 405
    if current_user.tipologia == 'cliente':
        return render_template('405.html'), 405
    
    viaggio = request.form.to_dict()
    continente = viaggio.get('continente')
    nazione = viaggio.get('nazione')
    data = viaggio.get('data')
    num_giorni = int(viaggio.get('num_giorni'))
    aeroporto = viaggio.get('aeroporto')
    prezzo = int(viaggio.get('prezzo'))
    descrizione = viaggio.get('descrizione')
    titolo = viaggio.get('titolo')

    if continente == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if nazione == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if data == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if num_giorni == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if aeroporto == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if prezzo == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if descrizione == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    if titolo == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('area_personale'))
    
    if continente != "Europa" and continente != "Asia" and continente != "Africa" and continente != "Oceania" and continente != "NordAmerica" and continente != "SudAmerica":
        flash("Il continente selezionato non è disponibile", 'warning')
        return redirect(url_for('area_personale'))
    if num_giorni < 5 or num_giorni > 21:
        flash('Devi inserire un numero di giorni valido!', 'danger')
        return redirect(url_for('area_personale'))
    if prezzo < 0:
        flash('Non puoi inserire un prezzo negativo per il viaggio!', 'danger')
        return redirect(url_for('area_personale'))
    if ('.' or ',') in str(prezzo):
        flash('Puoi inserire solamente prezzi mensili interi!', 'warning')
        return redirect(url_for('area_personale')) 
    if len(descrizione) < 100:
        flash('La descrizione deve essere formata da un minimo di 100 caratteri', 'danger')
        return redirect(url_for('area_personale'))
    if len(titolo) < 3 or len(titolo) > 70:
        flash('Il requisito sulla lunghezza del titolo non è rispettato. Deve avere un numero di caratteri compreso fra 3 e 40!', 'danger')
        return redirect(url_for('area_personale'))
    
    
    # Se esiste già un viaggio approvato per la stessa destinazione, nella stessa data in cui il coordinatore sta provando a inserire il suo viaggio, automaticamente non potrà andare avanti con la richiesta!
    viaggioEsistente = viaggi_dao.getViaggioEsistente(nazione, data)
    if viaggioEsistente:
        flash(f'Esiste già un viaggio approvato in data {data} per la nazione {nazione}! Riprova in un altro giorno.', 'warning')
        return redirect(url_for('area_personale'))

    img_viaggio = request.files.get('immagine')
    if not img_viaggio:
        flash('Devi inserire obbligatoriamente un\'immagine del viaggio!', 'warning')
        return redirect(url_for('area_personale'))
    
    nuovo_viaggio = {
        'id_coordinatore': current_user.id,
        'continente': continente,
        'nazione': nazione,
        'data': data,
        'num_giorni': num_giorni,
        'aeroporto': aeroporto,
        'prezzo': prezzo,
        'descrizione': descrizione,
        'titolo': titolo
    }
    
    if current_user.tipologia == 'admin':
        nuovo_viaggio['approvato'] = 1
    else:
        nuovo_viaggio['approvato'] = 0

    secondi = datetime.now().timestamp()

    img = Image.open(img_viaggio)

    width, height = img.size
    new_width = JOURNEY_IMG_HEIGHT * width / height

    size = new_width, JOURNEY_IMG_HEIGHT
    img.thumbnail(size, Image.Resampling.LANCZOS)

    left = (new_width/2 - JOURNEY_IMG_HEIGHT/2)
    top = 0
    right = (new_width/2 + JOURNEY_IMG_HEIGHT/2)
    bottom = JOURNEY_IMG_HEIGHT

    img = img.crop((left, top, right, bottom))

    ext = img_viaggio.filename.split('.')[-1]

    img.save('static/viaggio/' + '@Viaggio' + '.' + str(current_user.id) + '.' + str(secondi) + '.' + ext)

    img_viaggio = '@Viaggio' + '.' + str(current_user.id) + '.' + str(secondi) + '.' + ext
    nuovo_viaggio['img_viaggio'] = img_viaggio

    success = viaggi_dao.inserisciViaggio(nuovo_viaggio)
    if not success:
        flash('Si sono verificati degli errori nell\'inserimento dell\'annuncio del viaggio, riprova tra qualche minuto!', 'danger')
        return redirect (url_for('area_personale'))
    else:
        id_viaggio = viaggi_dao.getIdViaggio(nuovo_viaggio)['id']
        successPartecipazione = viaggi_dao.inserisciPartecipazioneViaggio(current_user.id, id_viaggio)
        if current_user.tipologia == 'admin':
            if not successPartecipazione:
                flash('Qualcosa è andato storto...', 'warning')
                return redirect(url_for('area_personale'))
            else:
                flash('L\'annuncio del viaggio è stato inserito con successo! Ora potrai visualizzarlo nella homepage del sito!', 'success')
                return redirect (url_for('area_personale'))
        else:
            if not successPartecipazione:
                flash('Qualcosa è andato storto...', 'warning')
                return redirect(url_for('area_personale'))
            else:
                flash('L\'inserimento dell\'annuncio del viaggio è andato a buon fine! Ora dovrà essere approvato dall\'amministratore prima di essere pubblicato nella homepage del sito!', 'success')
                return redirect (url_for('area_personale'))
            

@app.route('/viaggio/<int:id_viaggio>/modifica_viaggio', methods=['POST'])
@login_required
def modifica_viaggio(id_viaggio):
    viaggio_esistente = viaggi_dao.getViaggio(id_viaggio)

    if viaggio_esistente['id_coordinatore'] != current_user.id:
        return render_template('405.html'), 405
    
    if current_user.tipologia == 'cliente':
        return render_template('405.html'), 405
    
    viaggio = request.form.to_dict()
    data = viaggio.get('data')
    num_giorni = int(viaggio.get('num_giorni'))
    aeroporto = viaggio.get('aeroporto')
    prezzo = int(viaggio.get('prezzo'))
    descrizione = viaggio.get('descrizione')
    titolo = viaggio.get('titolo')


    if data == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if num_giorni == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if aeroporto == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if prezzo == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if descrizione == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if titolo == "":
        flash('Devi compilare tutti i campi!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    
    if num_giorni < 5 or num_giorni > 21:
        flash('Devi inserire un numero di giorni valido!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if prezzo < 0:
        flash('Non puoi inserire un prezzo negativo per il viaggio!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if ('.' or ',') in str(prezzo):
        flash('Puoi inserire solamente prezzi mensili interi!', 'warning')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if len(descrizione) < 100:
        flash('La descrizione deve essere formata da un minimo di 100 caratteri', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    if len(titolo) < 3 or len(titolo) > 70:
        flash('Il requisito sulla lunghezza del titolo non è rispettato. Deve avere un numero di caratteri compreso fra 3 e 40!', 'danger')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    
    
    # Se esiste già un viaggio approvato per la stessa destinazione, nella stessa data in cui il coordinatore sta provando a inserire il suo viaggio, automaticamente non potrà andare avanti con la richiesta!
    if data != viaggio_esistente['data']:
        nazione = viaggio_esistente['nazione']
        viaggioStessaDataENazione = viaggi_dao.getViaggioEsistente(nazione, data)
        if viaggioStessaDataENazione:
            flash(f'Esiste già un viaggio approvato in data {data} per la nazione {nazione}! Riprova in un altro giorno.', 'warning')
            return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    
    nuovo_viaggio = {
        'data': data,
        'num_giorni': num_giorni,
        'aeroporto': aeroporto,
        'prezzo': prezzo,
        'descrizione': descrizione,
        'titolo': titolo
    }

    img_viaggio = request.files.get('img_viaggio')
    if img_viaggio:
        os.remove('static/viaggio/'+viaggio_esistente['img_viaggio'])
        img = Image.open(img_viaggio)

        width, height = img.size
        new_width = JOURNEY_IMG_HEIGHT * width / height

        size = new_width, JOURNEY_IMG_HEIGHT
        img.thumbnail(size, Image.Resampling.LANCZOS)

        left = (new_width/2 - JOURNEY_IMG_HEIGHT/2)
        top = 0
        right = (new_width/2 + JOURNEY_IMG_HEIGHT/2)
        bottom = JOURNEY_IMG_HEIGHT

        img = img.crop((left, top, right, bottom))

        ext = img_viaggio.filename.split('.')[-1]
        secondi = datetime.now().timestamp()

        img.save('static/viaggio/' + '@Viaggio' + '.' + str(current_user.id) + '.' + str(secondi) + '.' + ext)

        img_viaggio = '@Viaggio' + '.' + str(current_user.id) + '.' + str(secondi) + '.' + ext

        successFoto = viaggi_dao.modificaImmagineViaggio(img_viaggio, id_viaggio)
    else:
        successFoto = True

    successInfo = viaggi_dao.modificaInformazioniViaggio(nuovo_viaggio, id_viaggio)

    if successFoto and successInfo:
        flash('L\'annuncio del viaggio è stato modificato con successo!', 'success')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))
    else:
        flash('Si sono verificati degli errori nella modifica dell\'annuncio...', 'warning')
        return redirect(url_for('pagina_viaggio', id_viaggio = id_viaggio))


@app.route('/viaggio/<int:id_viaggio>/lista_partecipanti', methods = ['POST', 'GET'])
@login_required
def lista_partecipanti(id_viaggio):
    viaggio = viaggi_dao.getViaggio(id_viaggio)

    if viaggio['id_coordinatore'] != current_user.id:
        return render_template('405.html'), 405

    partecipazioni = viaggi_dao.getPartecipazioniViaggio(id_viaggio)

    return render_template("lista_partecipanti.html", partecipazioni = partecipazioni, viaggio = viaggio)



@app.route('/lista_utenti', methods=['POST', 'GET'])
@login_required
def lista_utenti():
    if current_user.tipologia != 'admin':
        return render_template('405.html'), 405
    
    users_list = utenti_dao.getUtenti()
    return render_template('lista_utenti.html', users_list = users_list)


@app.route('/lista_utenti/upgradeCoordinatore/<int:id_utente>', methods=['POST'])
@login_required
def upgradeCoordinatore(id_utente):
    success = utenti_dao.modificaTipologiaUtente(id_utente)
    if success:
        flash('L\'utente è stato promosso a coordinatore con successo!', 'success')
    else:
        flash('Si sono verificati degli errori nella procedura, riprova più tardi!', 'warning')

    return redirect(url_for('lista_utenti'))


@app.route('/lista_utenti/ban/<int:id_utente>', methods=['POST'])
@login_required
def ban(id_utente):
    success = utenti_dao.banUtente(id_utente)
    if success:
        flash('L\'utente è stato bannato con successo!', 'success')
    else:
        flash('Si sono verificati degli errori nella procedura, riprova più tardi!', 'warning')

    return redirect(url_for('lista_utenti'))

@app.route('/approvazione_viaggi', methods=['GET', 'POST'])
@login_required
def approvazione_viaggi():
    if current_user.tipologia != 'admin':
        return render_template('405.html'), 405
    
    viaggi_in_approvazione = viaggi_dao.getViaggiInApprovazione()
    
    return render_template('approvazione_viaggi.html', viaggi_in_approvazione = viaggi_in_approvazione)


@app.route('/approvazione_viaggi/approvazione/<int:id_viaggio>', methods = ['POST'])
@login_required
def changeApprovazione(id_viaggio):
    if current_user.tipologia != 'admin':
        return render_template('405.html'), 405
    
    success = viaggi_dao.changeApprovazioneViaggio(id_viaggio)

    if success:
        flash('Il viaggio è stato approvato con successo! Ora tutti gli utenti del sito potranno visualizzarlo nella homepage e avranno la possibilità di parteciparvi!', 'success')
        return redirect(url_for('approvazione_viaggi'))
    else:
        flash('Si sono verificati degli errori nell\'approvazione del viaggio...', 'warning')
        return redirect(url_for('approvazione_viaggi'))
    
@app.route('/pagina_prenotazione/<int:id_viaggio>/<int:id_utente>', methods = ['POST', 'GET'])
@login_required
def pagina_prenotazione(id_viaggio, id_utente):
    if current_user.id != id_utente:
        return render_template('405.html'), 405
    
    viaggio = viaggi_dao.getViaggio(id_viaggio)
    utente = utenti_dao.getUtenteByID(id_utente)

    return render_template('pagina_prenotazione.html', viaggio = viaggio, utente = utente)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@login_manager.unauthorized_handler
@app.errorhandler(405)
def unauthorized(e):
    return render_template('405.html'), 405


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    db_user = utenti_dao.getUtenteByID(user_id)
    if db_user is not None:
        user = User(id=db_user['id'], nome = db_user['nome'], cognome = db_user['cognome'], email = db_user['email'], password = db_user['password'], tipologia = db_user['tipologia'], img_profilo=db_user['img_profilo'])
    return user