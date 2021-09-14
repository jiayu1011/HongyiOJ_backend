import datetime

# 从P10000开始, P10001, P10002
from django.http import JsonResponse

from HongyiOJ.token import *


def generateProblemId(seqNum):
    seq = 10000 + seqNum

    problemId = 'P' + str(seq)
    return problemId


def generateContestId(seqNum):
    seq = 10000 + seqNum

    contestId = 'C' + str(seq)
    return contestId


def generateDiscussionId(seqNum):
    seq = 10000 + seqNum

    discussionId = 'D' + str(seq)
    return discussionId


def generateEvaluationId(seqNum):
    seq = 10000 + seqNum

    evaluation = 'E' + str(seq)
    return evaluation


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


def getCodeFileSuffix(codeLanguage):
    clArr = ['C', 'C++', 'Python3', 'Java']
    suffixArr = ['.c', '.cpp', '.py', '.java']

    if codeLanguage not in clArr:
        return '.txt'

    return suffixArr[clArr.index(codeLanguage)]


if __name__ == "__main__":
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    a = {
        'add': 123,
        'sss': 111
    }
    for key in a:
        print(key)
