import datetime

# 从P10000开始, P10001, P10002
import os

from django.http import JsonResponse

from HongyiOJ.token import *
import HongyiOJ.config as BackendConfig


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

# 'C++' -> '.cpp'
def getCodeFileSuffix(codeLanguage):
    suffixDic = BackendConfig.Config.codeSuffixDic

    if codeLanguage not in suffixDic:
        return '.txt'

    return suffixDic[codeLanguage]

# '.cpp' -> 'C++'
def getCodeLanguage(suffix):
    suffixDic = BackendConfig.Config.codeSuffixDic
    for key in suffixDic:
        if suffixDic[key] == suffix:
            return key

    return ''

def formatCodeFile(evaluationId, codeLanguage):
    return '{}_code{}'.format(evaluationId, getCodeFileSuffix(codeLanguage))

def formatOutputFile(evaluationId):
    return '{}_output.txt'.format(evaluationId)

def formatOutputFolder(evaluationId):
    return '{}_output'.format(evaluationId)


if __name__ == "__main__":
    print(formatCodeFile(evaluationId='E10001', codeLanguage='Python3'))
    print(formatOutputFile('E10002'))
    print(getCodeLanguage('.py'))
    print(os.getcwd())
    a = '\n' +\
        '   ' +\
        'as  dd' +\
        '   ' +\
        '\n'

    print('\n 1 2  '.split())