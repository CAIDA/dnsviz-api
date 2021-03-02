import json

from flask import current_app
from flask_restful import Resource

class Routes(Resource):
    def get(self):
        '''Output list of all active endpoints'''
        endpoints = {}
        for rule in current_app.url_map.iter_rules():
            # remove blueprint name from endpoint name
            endpoint_name = rule.endpoint.split('.')[-1]
            # Split endpoint route and remove argument definitions
            endpoint_path_parts = rule.rule.split('/')[:-1]
            endpoint_path = '/'.join(endpoint_path_parts) + "/"
            # Readd argument names
            if len(rule.arguments) > 0:
                endpoint_argument = list(rule.arguments)[0]
                endpoint_path += f"<{endpoint_argument}>" 
            # Skip root path
            if endpoint_path != '/':
                endpoints[endpoint_name] = endpoint_path
        return endpoints