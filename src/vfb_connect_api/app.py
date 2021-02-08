from flask import Flask, Blueprint
from vfb_connect_api import settings
from vfb_connect_api.restplus import api
from vfb_connect_api.endpoints.vfb_connect_api import ns as api_namespace

app = Flask(__name__)

blueprint = Blueprint('vfb_connect_api', __name__, url_prefix='/vfb_connect_api')


def configure_app(flask_app):
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    api.init_app(blueprint)
    api.add_namespace(api_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(app)
    app.run(host="0.0.0.0", port="5000",debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    main()
