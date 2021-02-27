class DatabaseConnection:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close(*args)

    '''Base class for database connection'''
    def query(self, query:str)->dict:
        pass