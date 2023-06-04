from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials"
        self.headers = {"WWW-Authenticate": "Bearer"}


class LoginException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = 'Incorrect username or password'
        self.headers = {"WWW-Authenticate": "Bearer"}
