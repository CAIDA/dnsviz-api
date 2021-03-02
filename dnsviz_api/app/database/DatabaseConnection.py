from flask import current_app

from dnsviz_api.app.utils.extension import FlaskExtension

class DatabaseConnection(FlaskExtension):
    '''Base class for database connection extension'''

    def connect(self):
        '''Connect to database'''
        pass

    def teardown(self):
        '''Close database connection'''
        pass

    '''Base class for database connection'''
    def query(self, query:str)->dict:
        pass