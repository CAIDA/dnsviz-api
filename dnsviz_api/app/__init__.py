import sys

from flask import Flask, Blueprint
from flask_restful import Api

from dnsviz_api.app.resources.TrustTree import TrustTree

def create_app(app_config:'Config' = None) -> Flask:
    '''Flask application factory
    
    Args:
        app_config: Defaults to None. Contain application config values.

    Returns:
        Configured Flask app

    '''
    app = Flask(__name__)
    if app_config is not None:
        app.config.from_object(app_config)

    with app.app_context():

        api_bp = Blueprint('api_bp', __name__)
        api = Api(api_bp)

        api.add_resource(TrustTree, '/trust-tree', '/trust-tree/<string:hostname>')

        app.register_blueprint(api_bp)

        return app



