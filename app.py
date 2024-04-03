# pip install flask
from flask import Flask, render_template, request, url_for, redirect, flash
# pip install flask_login
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# pip install werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
# pip install Pillow
from PIL import Image

from models import User
import utenti_dao


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkdwIO3KSoso2oi1393JDI2k2k1'

login_manager = LoginManager()
login_manager.init_app(app)

PROFILE_IMG_HEIGHT = 160


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

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
        new = User(id=utente['id'], nome = utente['nome'], cognome = utente['cognome'], email = utente['email'], password = utente['password'], tipologia = utente['tipologia'], img_profilo = utente['img_profilo'])
        login_user(new)
        return redirect(url_for('index'))

    else:
        flash('La mail e/o la password inserita non è corretta', 'danger')
        return redirect(url_for('login_page'))
    

@app.route('/profilo')
@login_required
def area_personale():
    return render_template('profilo.html')

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