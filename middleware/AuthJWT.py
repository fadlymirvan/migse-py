from flask import request

from utils import Auth
from models import Token


def CheckJWT():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return False, "Bearer Token Error", 401

    else:
        auth_token = ""

    if auth_token is not "":
        data = Auth.decode_token(auth_token)
        isUsed = Token.check_token(auth_token)
        if not isUsed:
            return True, data['data']['user_id'], auth_token
        else:
            return False, "Invalid Token", auth_token

    return False, "Bearer Token Error", auth_token


