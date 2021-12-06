from flask import Blueprint
import dash


def create_dash_applcation(flask_app):

    dash_app = dash.Dash(server=flask_app, name="Dashboard", 
    url_base_path_name='/dashboard')

    return dash_app

from app.dashboard import figures