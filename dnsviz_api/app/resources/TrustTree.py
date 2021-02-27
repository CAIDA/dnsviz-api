import os

from flask_restful import Resource

from dnsviz_api.app.database.DGraphConnection import DGraphConnection

TRUST_TREE_QUERY = '''
    query q($descriptor: string) {
        var(func: eq(descriptor, $descriptor)) @recurse{
            p as authNsParent
            c as authNsChild
            pr as parentDomain
        }
        var(func: eq(descriptor, $descriptor)){
            id as uid
        }
        q(func: uid(p, c, pr, id)){
            uid
            xid
            dgraph.type,
            name: descriptor
            authNsParent{
                uid
            }
            authNsChild{
                uid
            }
            parentDomain{
                uid
            }
        }
    }
'''


class TrustTree(Resource):
    '''The TrustTree resource represents the collections of dependencies
    for a given hostname
    '''
    def get(self, hostname):
        # Format hostname to lowercase with trailing period
        descriptor = hostname.lower()
        if descriptor[-1] != '.':
            descriptor = f'{descriptor}.'
        DATABASE_URI=os.getenv('DATABASE_URI')
        with DGraphConnection(DATABASE_URI) as db:
            return db.query(TRUST_TREE_QUERY, {'$descriptor':'google.com.'})