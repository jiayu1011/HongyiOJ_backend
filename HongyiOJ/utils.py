import datetime

# 从P10000开始, P10001, P10002
import os

from django.http import JsonResponse

from HongyiOJ.token import *
import HongyiOJ.config as HostConfig



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
    suffixDic = HostConfig.Config.codeSuffixDic

    if codeLanguage not in suffixDic:
        return '.txt'

    return suffixDic[codeLanguage]

# '.cpp' -> 'C++'
def getCodeLanguage(suffix):
    suffixDic = HostConfig.Config.codeSuffixDic
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


def getAnalyzeResult(resultFilePath) -> dict:
    with open(f'{resultFilePath}/{HostConfig.Config.analyzeResFileName}', 'r') as f:
        resArr = f.readlines()
    resDict = {}
    if len(resArr) < 3:
        return resDict

    resDict['result'] = resArr[0].strip()
    if resDict['result'] in [
        HostConfig.Config.COMPILE_ERROR,
        HostConfig.Config.RUNTIME_ERROR
    ]:
        resDict['errLog'] = ''.join(resArr[1:])
        return resDict

    resDict['timeCost'] = resArr[1].strip()
    resDict['memoryCost'] = resArr[2].strip()

    if resDict['result']==HostConfig.Config.WRONG_ANSWER:
        if len(resArr) < 6:
            return resDict
        resDict['stdInputCase'] = resArr[3].strip()
        resDict['stdOutputCase'] = resArr[4].strip()
        resDict['dockerOutputCase'] = resArr[5].strip()


    return resDict

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