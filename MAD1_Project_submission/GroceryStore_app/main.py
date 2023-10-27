import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

def is_logged_in(role):
    return session.get(role)

app = None

def create_app():
    
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)  
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
app.secret_key = 'Nandu_app_key'

from application.controllers import *

if __name__ == '__main__':
  
  app.run(host='0.0.0.0',port=8080)
