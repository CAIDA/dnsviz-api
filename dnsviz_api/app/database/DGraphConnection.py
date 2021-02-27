import json

import pydgraph

from dnsviz_api.app.database.DatabaseConnection import DatabaseConnection

class DGraphConnection(DatabaseConnection):
    '''Class for dgraph database connection'''
    def __init__(self, conn_str):
        print(conn_str)
        self.client_stub = pydgraph.DgraphClientStub(conn_str)
        self.client = pydgraph.DgraphClient(self.client_stub)

    def close(self, *args):
        # Close each DGraph client stub
        self.client_stub.close()

    def query(self, query:str, variables:dict) -> dict:
        print(variables)
        res = self.client.txn(read_only=True).query(query, variables=variables)
        data = json.loads(res.json)
        return data
