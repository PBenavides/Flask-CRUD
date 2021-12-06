"""
Oracle database connection.
Este script se encarga de definir la conexion-desconexion de la bd
"""

import cx_Oracle
from config import Config
from flask import g

HOST = 'localhost'
user = 'system'
password = 'admin'
PORT = '1521'
SERVICE = 'xe'

dsn = HOST + ':'+PORT+'/'+SERVICE
#En esta app no hay schema interno, es decir, no se levanta la BD por si misma.

# Hacemos un get_db(). para poder importar la conexion como global
def get_db():
    """ conectar la bd, amarrarla a la app global (g) y
    retornar un g.db: conexion y g.cur: cursor
    """
    if ("db" not in g) or ("cur" not in g):
        
        g.db = cx_Oracle.connect(user, password, dsn)  #Defino la conexion
        g.cur = g.db.cursor()  #Defino mi cursor

    return g.db, g.cur

def close_db(e=None):
    """ Cerramos la conexion """
    cur = g.pop("cur", None)
    if cur is not None:
        cur.close()
    
    db = g.pop("db", None)
    if db is not None:
        db.commit()
        db.close()

def rollback_db(e=None):
    """Rollback de la BD"""
    db = g.pop("db", None)
    if db is not None:
        db.rollback()
        db.close()