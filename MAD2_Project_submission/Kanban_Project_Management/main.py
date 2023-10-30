import os
from flask import Flask
from application import config
from application import workers
from flask_restful import Resource, Api
from application.config import LocalDevelopmentConfig
from application.config import Config
from application.database import db
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role
from flask_cors import CORS

app = None
api = None
celery = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    CORS(app)
    app.config.from_object(Config)  
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    celery = workers.celery

    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = "Asia/Calcutta",
        enable_utc = False
    )

    celery.Task = workers.ContextTask
    app.app_context().push()

    return app, api, celery

app, api, celery = create_app()


from application.api import ListAPI
api.add_resource(ListAPI, "/api/<string:username>", "/api/<string:username>/<int:list_id>")

from application.api import CardAPI
api.add_resource(CardAPI, "/api/<string:username>/cards", "/api/<string:username>/cards/<int:list_id>","/api/<string:username>/cards/<int:list_id>/<int:card_id>")

from application.api import TimelineAPI
api.add_resource(TimelineAPI, "/api/<string:username>/timeline")

from application.api import CompstatAPI
api.add_resource(CompstatAPI, "/api/<string:username>/compstat")

from application.api import ExportAPI
api.add_resource(ExportAPI, "/api/<string:username>/export")

from application.api import ListexportAPI
api.add_resource(ListexportAPI, "/api/<string:username>/<int:list_id>/export")

from application.api import SummaryAPI
api.add_resource(SummaryAPI, "/api/<string:username>/sumtable")

from application.controllers import *

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)
