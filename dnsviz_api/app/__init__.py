import sys

from flask import Flask, Blueprint
from flask_restful import Api

from dnsviz_api.app.resources.Routes import Routes
from dnsviz_api.app.resources.Search import Search
from dnsviz_api.app.resources.TrustTree import TrustTree

from dnsviz_api.app.extensions import cors, talisman, db

def create_app(app_config:'Config' = None) -> Flask:
    '''Flask application factory
    
    Args:
        app_config: Defaults to None. Contain application config values.

    Returns:
        Configured Flask app

    '''
    app = Flask(__name__, static_folder=None)

    # Enable CORS
    cors.init_app(app)
    db.init_app(app)

    if app_config is not None:
        app.config.from_object(app_config)

    with app.app_context():
        # Set security headers for production
        if app.config['USE_TALISMAN']:
            talisman.init_app(app)

        api_bp = Blueprint('api_bp', __name__)
        api = Api(api_bp)

        register_resources(api)

        app.register_blueprint(api_bp)

        return app

def register_resources(api):
    api.add_resource(Routes, '/', endpoint='routes')
    api.add_resource(Search, '/search/<string:query>', endpoint='search')
    api.add_resource(TrustTree, '/trust-tree/<string:hostname>', endpoint='trust-tree')




