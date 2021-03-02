import json

from flask import current_app, _app_ctx_stack
import pydgraph

from dnsviz_api.app.database.DatabaseConnection import DatabaseConnection

class DGraphConnection(DatabaseConnection):
    '''Class for dgraph database connection'''

    def close(self, *args):
        # Close each DGraph client stub
        self.client_stub.close()

    def connect(self):
        client_stub = pydgraph.DgraphClientStub(current_app.config['DATABASE_URI'])
        client = pydgraph.DgraphClient(client_stub)
        return (client_stub, client)

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'dgraph_client_stub'):
            ctx.dgraph_client_stub.close()

    def query(self, query:str, variables:dict) -> dict:
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'dgraph_client_stub'):
                client_stub, client = self.connect()
                ctx.dgraph_client_stub = client_stub
                ctx.dgraph_client = client
            res = ctx.dgraph_client.txn(read_only=True).query(query, variables=variables)
            data = json.loads(res.json)
            return data
