import logging

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS

from app.env_variables import SQLALCHEMY_DATABASE_URI

from app.cors.configuration import CORS_CONFIG
from app.email.configuration import MAIL_SETTINGS, MailSender
from app.db.configuration import sa
from app.security.configuration import configure_security
from app.resources.configuration import FileUploadConfig

from app.route.user import (
    UserResource,
    UserActivationResource
)
from app.route.blueprints import cars_blueprint


# ----------------------------------------------------------------------
# LOGGER CONFIGURATION
# ----------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def main() -> Flask:

    with app.app_context():

        # ----------------------------------------------------------------------
        # DB CONFIGURATION
        # ----------------------------------------------------------------------
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        # ----------------------------------------------------------------------
        # REST API CONFIGURATION
        # ----------------------------------------------------------------------
        api = Api(app)
        api.add_resource(UserResource, '/users')
        api.add_resource(UserActivationResource, '/users/activate')

        # ----------------------------------------------------------------------
        # EMAIL CONFIGURATION
        # ----------------------------------------------------------------------
        app.config.update(MAIL_SETTINGS)
        MailSender.init(app)

        # ----------------------------------------------------------------------
        # SECURITY CONFIGURATION
        # ----------------------------------------------------------------------
        configure_security(app)

        # ----------------------------------------------------------------------
        # CORS CONFIGURATION
        # ----------------------------------------------------------------------
        CORS(app, resources={
            '/*': CORS_CONFIG
        })

        # ----------------------------------------------------------------------
        # AWS CONFIGURATION
        # ----------------------------------------------------------------------
        @app.route("/file", methods=['POST'])
        def upload_file():
            file_upload_config = FileUploadConfig(request)
            return file_upload_config.send_to_aws(), 201

        # ----------------------------------------------------------------------
        # BLUEPRINTS REGISTRATION
        # ----------------------------------------------------------------------
        app.register_blueprint(cars_blueprint)

        # ----------------------------------------------------------------------
        # GLOBAL EXCEPTION HANDLING
        # ----------------------------------------------------------------------
        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            logging.info('Default error: ', error)
            logging.info(error.args)
            return {'message': str(error)}, 500

        @app.route('/error_test')
        def test_error():
            if 1 == 1:
                raise ValueError('Error')


        return app
