import dash
from flask import Flask
from config import Config
from flask.helpers import get_root_path
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_class = Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['MONGO_DBNAME'] = 'pythonmongodb'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

    mongo.init_app(app)
    

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    print('main bp importado y registrado')
    from app.crud_queries import bp as crud_bp
    app.register_blueprint(crud_bp)
    print('crud bp importado y registrado')
    app.app_context().push()
    register_dashapp(app)

    
    return app

def register_dashapp(app):
    """Registro la aplicación de Dash
    """

    from app.dashboard.layout import layout
    #from app.dashboard.callbacks import register_callbacks

    # Esto es un wrapper
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp.title = "DashApp"
        dashapp.layout = layout #Acá le agregamos el layout que cargamos al principio
    


    

from app import database