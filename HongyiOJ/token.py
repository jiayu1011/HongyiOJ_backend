"""
for token generation and validation
"""

import jwt
from jwt import exceptions
import json
import time

SECRET_KEY = "asgfddasdasdasgerher"



def createToken(name):
    """
    Token generation
    :param name: username
    :return: token: token for Authorization in http headers
    """

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


def validateToken(token):
    """
    Token validation
    :param token: token created by backend
    :return:
    payload: secret information
    msg: exception message, will be None when validate success
    """

    global SECRET_KEY
    payload = None
    msg = None

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms='HS256')

    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'

    return payload, msg


if __name__=='__main__':
    t = createToken('qwer')
    print(t)
    p, m = validateToken(t)
    print(p, m)



