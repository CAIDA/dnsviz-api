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
            node_uid as uid
        }
        var(func: eq(descriptor, $descriptor)){
            id as uid
        }
        var(func: uid(p, c)){
            rp as ~authNsParent
            rc as ~authNsChild
        }
        var(func: uid(node_uid)){
            rpd as ~parentDomain (first:5) @filter(eq(dgraph.type, nameserver)){
                pd_rp as ~authNsParent
                pd_rc as ~authNsChild 
            }
        }
        q(func: uid(p,c, pd, id, ip4, ip6)){
            uid
            dgraph.type
            expand(_all_){
                uid
            }
        }
        domain_borders(func: uid(rp, rc, pd_rp, pd_rc)){
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
        ns_borders(func: uid(rpd)){
            uid
            xid
            dgraph.type,
            descriptor
            isMapped
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
        current_app.logger.info(f"Received request for TrustTree endpoint")
        current_app.logger.info(f"TrustTree query: '{hostname}'")
        descriptor = hostname.lower()
        if descriptor[-1] != '.':
            descriptor = f'{descriptor}.'
        hostname_data = db.query(TRUST_TREE_QUERY, {'$descriptor':descriptor})
        if len(hostname_data['q']) > 0:
            parsed_hostname_data = {
                'q':hostname_data['q']
            }
            parsed_hostname_data['borders'] = []
            border_type_list = ('domain_borders', 'ns_borders')
            for border_type in border_type_list:
                if border_type in hostname_data:
                    for node in hostname_data[border_type]:
                        parsed_hostname_data['borders'].append(node)
            return parsed_hostname_data
        else:
            return invalid_hostname_error()
