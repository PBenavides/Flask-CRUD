from flask import Flask
from config import Config

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

    return app