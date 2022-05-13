import os

import werkzeug
from flask import Flask
from flask_cors import CORS

werkzeug.cached_property = werkzeug.utils.cached_property
import flask.scaffold

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

from backend.app.configs import Configs
from backend.app.core.utils.logger import get_logger, log_request

logger = get_logger()
db = SQLAlchemy()


def create_app(app_configs):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": app_configs.CORS_ORIGINS,
                                 "expose_headers": ["Origin", "X-Requested-With", "Content-Type", "Accept"],
                                 "supports_credentials": True}})

    @app.after_request
    def log_incoming_request(response):
        log_request(app, response)
        return response

    app.config.from_object(app_configs)
    app.secret_key = app_configs.SECRET_KEY
    app.config['RESTPLUS_MASK_SWAGGER'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getcwd()}/test.db'
    db.init_app(app)
    app.db = db

    @app.before_first_request
    def setup_db():
        db.create_all()

    api = Api(app, doc='/docs')

    from backend.app.auth.controllers.auth_controller import api as auth_api
    from backend.app.auth.controllers.user_controller import api as user_api
    from backend.app.banking.controllers.account_controller import api as account_api
    from backend.app.banking.controllers.transaction_controller import api as transaction_api
    api.add_namespace(auth_api)
    api.add_namespace(user_api)
    api.add_namespace(account_api)
    api.add_namespace(transaction_api)

    # set_api(api)
    return app