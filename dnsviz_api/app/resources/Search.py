from difflib import SequenceMatcher

from flask import current_app
from flask_restful import Resource

from dnsviz_api.app.extensions import db

HOST_SEARCH_QUERY = '''
    query search_results($descriptor: string){
        search_results(func: match(descriptor, $descriptor, 10), first: 10) @filter(
            eq(dgraph.type, [domain, ps_tld, tld])
        ){
            descriptor
            isMapped
            dgraph.type
        }
    }
'''

def create_term_comparator(term):
    b = term
    def calc_term_similarity(a):
        return SequenceMatcher(None, a['descriptor'], b).ratio()
    return calc_term_similarity

class Search(Resource):
    '''Endpoint for searching mapped hostnames'''
    def get(self, query):
        current_app.logger.info(f"Received request for Search endpoint")
        current_app.logger.info(f"Search query: '{query}'")
        descriptor = query.lower()
        search_data = db.query(HOST_SEARCH_QUERY, {'$descriptor':descriptor})
        # Return list of descriptors sorted by similarity to query
        search_term_comparator = create_term_comparator(descriptor)
        search_data['search_results'].sort(key=search_term_comparator, reverse=True)
        return search_data