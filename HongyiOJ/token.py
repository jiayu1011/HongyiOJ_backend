"""
for token generation and validation
"""

import jwt
from jwt import exceptions
import json
import time

SECRET_KEY = "asgfddasdasdasgerher"


"""
token generation
"""
def createToken(name):
    global SECRET_KEY
    headers = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    exp = int(time.time()+20)
    payload = {
        'name': name,
        'exp': exp
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm='HS256',
        headers=headers
    )



    return token



"""
token validation
"""
def validateToken(token):

    global SECRET_KEY
    payload = None
    msg = None

    try:
        payload = jwt.decode(token, SECRET_KEY, True, algorithms='HS256')

    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'

    return payload, msg




