from flask import Flask
from os import path


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .auth import auths
    from .view import view

    app.register_blueprint(auths, url_prefix='/')
    app.register_blueprint(view, url_prefix='/')


    return app