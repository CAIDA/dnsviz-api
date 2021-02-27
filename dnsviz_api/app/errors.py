from flask import abort

def invalid_hostname_error():
    return abort(404)