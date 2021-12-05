import os

from dotenv import load_dotenv


class Config():
    """Flask application config"""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    
    

    #Flask-MongoEngine settings
    

    #MONGODB_SETTING = {
    #    'db':'test',
    #    'host':'192.168.207.1',
    #    'port':27017
    #}