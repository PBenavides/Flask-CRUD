from flask import render_template, url_for, request, session, redirect
from app.main import bp
import bcrypt
from app import mongo

@bp.route('/')
def index():
    
    if 'username' in session:
        return 'Estas loggeado como ' + session['username']

    return render_template('main/index.html')

@bp.route('/login', methods=['POST'])
def login():

    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user: #If login_users exists, make validation
        if bcrypt.hashpw(request.form['pass'].encode['utf-8'],\
             login_user['password'].encode['utf-8']) == login_user['password'].encode('utf-8'):
            
            session['username'] = request.form['username']
            return redirect(url_for('main.index'))
        
    return 'Usuario o contraseña inválidos'
    

@bp.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        #Si existe un usuario, vamos a retornar el mensaje de que ya existe un usuario asi.
        users = mongo.db.users  #La coleccion users en MongoDB
        existing_user = users.find_one({'name': request.form['username']}) #Es username en el form. como id/name

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']

            return redirect(url_for('main.index'))

        return 'Este usuario ya existe'
    
    return render_template('main/register.html')