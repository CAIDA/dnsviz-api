from flask import current_app
from flask_restful import Resource

from dnsviz_api.app.extensions import db

HOST_SEARCH_QUERY = '''
    query search_results($descriptor: string){
        search_results(func: match(descriptor, $descriptor, 10), first: 10) @filter(
            eq(isMapped, true) AND 
            eq(dgraph.type, [domain, ps_tld, tld])
        ){
            descriptor
        }
    }
'''

class Search(Resource):
    '''Endpoint for searching mapped hostnames'''
    def get(self, query):
        current_app.logger.info(f"Received request for Search endpoint")
        current_app.logger.info(f"Search query: '{query}'")
        descriptor = query.lower()
        search_data = db.query(HOST_SEARCH_QUERY, {'$descriptor':descriptor})
        return search_data