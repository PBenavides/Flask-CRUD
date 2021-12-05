from flask import Blueprint
print('en __init__.py CORRIENDO BP CRUD QUERIES')
bp = Blueprint('crud_queries', __name__)
print('en __init__.py  hecho el bp')
from app.crud_queries import routes
print('en __init__.py  Importado el routes')