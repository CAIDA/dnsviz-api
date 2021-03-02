import os

from flask_restful import Resource

from dnsviz_api.app.errors import invalid_hostname_error
from dnsviz_api.app.extensions import db

TRUST_TREE_QUERY = '''
    query q($descriptor: string) {
        var(func: eq(descriptor, $descriptor)) @recurse{
            p as authNsParent
            c as authNsChild
            ip as ip4_glue
            pr as parentDomain
        }
        var(func: eq(descriptor, $descriptor)){
            id as uid
        }
        var(func: uid(p, c)){
            rp as ~authNsParent
            rc as ~authNsChild
        }
        q(func: uid(p,c, pr, id, ip)){
            uid
            xid
            dgraph.type,
            descriptor
            authNsParent{
                uid
            }
            authNsChild{
                uid
            }
            parentDomain{
                uid
            }
            ip4_glue{
                uid
            }
        }
        borders(func: uid(rp, rc)){
            uid
            xid
            dgraph.type,
            descriptor
            authNsParent{
                uid
            }
            authNsChild{
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
        current_app.logger.info(f"Received request for TrustTree endpoint")
        current_app.logger.info(f"TrustTree query: '{hostname}'")
        descriptor = hostname.lower()
        if descriptor[-1] != '.':
            descriptor = f'{descriptor}.'
        hostname_data = db.query(TRUST_TREE_QUERY, {'$descriptor':descriptor})
        if len(hostname_data['q']) > 0:
            return hostname_data
        else:
            return invalid_hostname_error()
