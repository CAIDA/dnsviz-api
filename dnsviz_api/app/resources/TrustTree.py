import os

from flask import current_app
from flask_restful import Resource

from dnsviz_api.app.errors import invalid_hostname_error
from dnsviz_api.app.extensions import db

TRUST_TREE_QUERY = '''
    query q($descriptor: string) {
        var(func: eq(descriptor, $descriptor)) @recurse{
            p as authNsParent
            c as authNsChild
            ip4 as ip4_glue
            ip6 as ip6_glue
            pd as parentDomain
        }
        var(func: eq(descriptor, $descriptor)){
            id as uid
        }
        var(func: uid(p, c)){
            rp as ~authNsParent
            rc as ~authNsChild
        }
        q(func: uid(p,c, pd, id, ip4, ip6)){
            uid
            dgraph.type
            expand(_all_){
                uid
            }
        }
        borders(func: uid(rp, rc)){
            uid
            xid
            dgraph.type,
            descriptor
            isMapped
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
