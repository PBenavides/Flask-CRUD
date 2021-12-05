from flask import render_template, url_for, request, session, redirect
from app.main import bp
import bcrypt
from app import mongo

@bp.route('/')
def index():
    
    try: 
        permit = session['username']
        print('SESSION USERNAME', session['username'])
    except:
        permit = "none"
    print('AUTH LEVEL:', permit)
    return render_template('main/index.html', session = session, permit=permit)

@bp.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name': request.form['username']})

        if login_user: #If login_users exists, make validation
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                
                session['username'] = request.form['username']
                return redirect(url_for('main.index'))
        
    return render_template('main/login.html')

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

@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.index')) 

