import datetime

# 从P10000开始, P10001, P10002
from django.http import JsonResponse

from HongyiOJ.token import *


def createProblemId(seqNum):

    seq = 10000 + seqNum

    problemId = 'P' + str(seq)
    return problemId


def removeDot(str):
    return ''.join(str.split('.'))


def isTokenAvailable(request):
    """

    :param request:
    :return:
    validate success - None
    validate error - errRes
    """
    res = {}
    clientToken = request.META['HTTP_AUTHORIZATION']
    payload, msg = validateToken(clientToken)
    if msg is not None:
        res['isOk'] = False
        res['errMsg'] = msg
        return res
    return None



if __name__=="__main__":
    print(removeDot('www.eee.rrr'))
    a = {
        '123': 'test',
        '456': 'te'
    }
    print(('12' or '46') in a)
