"""
django视图
"""

import random

# Create your views here.

from django.http import QueryDict

from HongyiOJ.models import *
from HongyiOJ.utils import *
from HongyiOJ.config import *
from HongyiOJ.response import *
import re

from django.core.mail import send_mail
from HongyiOJ_backend import settings
from HongyiOJ_evaluator.DockerConfig import docker
from HongyiOJ_evaluator.DockerScript import analyze

verifyDict = {}


def test(request):
    print(request)
    if request.method == 'GET':
        return HttpResponse('Welcome to Hongyi OJ!')
    else:
        return MyResponse.methodWrongRes


"""
---------------------------------------------
-----------------User Part-------------------
---------------------------------------------
"""


def login(request):
    """
    Login
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'POST':
        return MyResponse.methodWrongRes
    if not request.POST:
        return MyResponse.formEmptyRes

    print(request.POST)
    if not User.objects.filter(username=request.POST['username']).exists():
        res['isOk'] = False
        res['errMsg'] = '用户不存在'
        return JsonResponse(res)

    tempUserDict = User.objects.get(username=request.POST['username'])
    if request.POST['password'] != tempUserDict.password:
        res['isOk'] = False
        res['errMsg'] = '密码错误'
        return JsonResponse(res)

    token = createToken(request.POST['username'])

    res['userInfo'] = User.objects.filter(username=request.POST['username']).values()[0]
    res['token'] = token
    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)






def register(request):
    """
    Register
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'POST':
        return MyResponse.methodWrongRes
    if not request.POST:
        return MyResponse.formEmptyRes
    print(request.POST)
    POST_dict = request.POST.dict()

    if User.objects.filter(username=POST_dict['username']).exists():
        res['isOk'] = False
        res['errMsg'] = '用户名已经存在'
        return JsonResponse(res)
    elif User.objects.filter(email=POST_dict['email']).exists():
        res['isOk'] = False
        res['errMsg'] = '邮箱已被占用'
        return JsonResponse(res)


    if POST_dict['username'] == 'admin':
        POST_dict['identity'] = 'admin'
    User.objects.create(**POST_dict)

    res['userInfo'] = POST_dict
    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)




def getVerifyCode(request):
    """
    Get verify code
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'GET':
        return MyResponse.methodWrongRes
    if 'email' not in request.GET:
        return MyResponse.formEmptyRes

    sub = '欢迎使用Hongyi OJ!'

    targetEmail = request.GET['email']
    code = ''
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        code += ch
    msg = '您的验证码为：' + code


    send_mail(
        subject=sub,
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            targetEmail,
        ]
    )
    global verifyDict
    verifyDict[targetEmail] = code

    return MyResponse.defaultRes




def verify(request):
    """
    Verify
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == "POST":
        return MyResponse.methodWrongRes
    if ('email' or 'verifyCode') not in request.POST:
        return MyResponse.formEmptyRes

    global verifyDict
    print(verifyDict)
    if request.POST['email'] not in verifyDict:
        res['isOk'] = False
        res['errMsg'] = '邮箱错误'
        return JsonResponse(res)

    if not verifyDict[request.POST['email']] == request.POST['verifyCode']:
        res['isOk'] = False
        res['errMsg'] = '验证码错误'
        return JsonResponse(res)

    del verifyDict[request.POST['email']]
    return MyResponse.defaultRes




def resetPassword(request):
    print(request)
    res = {}
    if not request.method == 'PUT':
        return MyResponse.methodWrongRes
    PUT = QueryDict(request.body)

    if 'email' not in PUT and 'password' not in PUT:
        return MyResponse.formEmptyRes

    if not User.objects.filter(email=PUT['email']).exists():
        res['isOk'] = False
        res['errMsg'] = '邮箱未绑定账户'
        return JsonResponse(res)

    User.objects.filter(email=PUT['email']).update(password=PUT['password'])

    return MyResponse.defaultRes


def logout(request):
    """
    Log out
    :param request:
    PUT {username}
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'PUT':
        return MyResponse.methodWrongRes

    PUT = QueryDict(request.body)
    if 'username' not in PUT:
        return MyResponse.formEmptyRes

    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)


"""
---------------------------------------------
-----------------Problem Part----------------
---------------------------------------------
"""





def getProblemList(request):
    """
    Problem list
    :param request:
    GET {problemId|problemName, pageSize&currentPage, username， reviewStatus}
    ps: currentPage starts with 1
    :return:
    problemList: Array
    resultSum: Int
    """
    print(request)
    res = {}
    if not request.method == 'GET':
        return MyResponse.methodWrongRes
    # If user has logged in, validate his token
    if 'HTTP_AUTHORIZATION' in request.META:
        if not isTokenAvailable(request) is None:
            return JsonResponse(isTokenAvailable(request))


    problemList = []
    targetProblems = []
    doneList = []
    resultSum = 0


    if 'username' in request.GET:
        doneList = User.objects.get(username=request.GET['username']).acProblems.split(',')

    problems = Problem.objects.all()
    if 'reviewStatus' in request.GET:
        problems = Problem.objects.filter(reviewStatus=request.GET['reviewStatus'])

    problemDictArr = problems.values()

    if 'problemId' in request.GET:
        problemList.append(problems.filter(problemId=request.GET['problemId']).values()[0])
        resultSum = 1
        res['problemList'] = problemList
        res['resultSum'] = resultSum
        res['isOk'] = True
        res['errMsg'] = ''

        return JsonResponse(res)


    elif 'problemName' in request.GET:
        problemName = request.GET['problemName']
        names = []
        conditions = {}
        for item in problemDictArr:
            regExp = r'.*' + problemName + r'.*'
            # 正则匹配， re.I表示不区分大小写
            if re.search(regExp, item['name'], re.I) is not None:
                name = re.search(regExp, item['name'], re.I).group()
                names.append(name)

        for name in names:
            cds = conditions
            cds['problemName'] = name

            targetProblems.append(Problem.objects.filter(**cds).values()[0])

    if ('pageSize' or 'currentPage') not in request.GET:
        return MyResponse.formEmptyRes

    if 'problemName' in request.GET:
        resultSum = len(targetProblems)
        pageSize = int(request.GET['pageSize'])
        currentPage = int(request.GET['currentPage'])

        startSeq = min(pageSize * (currentPage - 1), resultSum)
        endSeq = min(pageSize * currentPage, resultSum)

        for i in range(startSeq, endSeq):
            item = targetProblems[i]
            if 'username' not in request.GET:
                item['isDone'] = False
            else:
                item['isDone'] = item['problemId'] in doneList

            problemList.append(item)

    else:
        resultSum = problems.count()
        pageSize = int(request.GET['pageSize'])
        currentPage = int(request.GET['currentPage'])

        startSeq = min(pageSize * (currentPage - 1), resultSum)
        endSeq = min(pageSize * currentPage, resultSum)

        for i in range(startSeq, endSeq):
            item = problemDictArr[i]
            if 'username' not in request.GET:
                item['isDone'] = False
            else:
                item['isDone'] = item['problemId'] in doneList

            problemList.append(item)

    # for item in problemList:
    #     del item['stdInput']
    #     del item['stdOutput']

    res['problemList'] = problemList
    res['resultSum'] = resultSum
    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)



def uploadProblem(request):
    """
    :param request:
    POST {problemName, problemTags, problemDiff, ...}
    all the attribute of Problem except for problemId(to be generated)
    :return: {
        isOk: '',
        errMsg: ''
    }
    """
    print(request)
    res = {}
    if not request.method == 'POST':
        return MyResponse.methodWrongRes
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))
    if not request.POST:
        return MyResponse.formEmptyRes
    POST_dict = request.POST.dict()
    seqNum = Problem.objects.count() + 1
    POST_dict['problemId'] = generateProblemId(seqNum)
    POST_dict['reviewStatus'] = 'reviewing'


    Problem.objects.create(**POST_dict)

    return MyResponse.defaultRes



"""
---------------------------------------------
-----------------Manage Part-----------------
---------------------------------------------
"""





def reviewProblem(request):
    """
    Review problems
    :param request:
    PUT {problemId, reviewStatus}
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'PUT':
        return MyResponse.methodWrongRes
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))

    PUT = QueryDict(request.body)
    if ('problemId' or 'reviewStatus') not in PUT:
        return MyResponse.formEmptyRes
    Problem.objects.filter(problemId=PUT['problemId']).update(reviewStatus=PUT['reviewStatus'])

    return MyResponse.defaultRes


def deleteProblem(request):
    """

    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'DELETE':
        return MyResponse.methodWrongRes
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))

    Problem.objects.filter(problemId=request.GET['problemId']).delete()



    return MyResponse.defaultRes




"""
---------------------------------------------
-----------------Evaluation Part-------------
---------------------------------------------
"""




def submitCode(request):
    """

    :param request: {author, relatedProblemId, codeLanguage, code}
    :return:
    """
    print(request)
    res = {}
    if request.method != 'POST':
        return MyResponse.methodWrongRes
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))
    if ('author' or 'relatedProblemId' or 'codeLanguage' or 'code') not in request.POST:
        return MyResponse.formEmptyRes

    POST_dict = request.POST.dict()
    seqNum = Evaluation.objects.count() + 1
    eId = generateEvaluationId(seqNum)
    POST_dict['evaluationId'] = eId
    POST_dict['submitTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    POST_dict['author'] = User(username=POST_dict['author'])
    rPId = POST_dict['relatedProblemId']
    POST_dict['relatedProblemId'] = Problem(problemId=POST_dict['relatedProblemId'])

    POST_dict['codeLength'] = len(POST_dict['code'])
    Evaluation.objects.create(**POST_dict)

    # Store recent code in the disk
    with open(
            Config.codeSubmitStorePath + '/' + formatCodeFile(evaluationId=eId, codeLanguage=POST_dict['codeLanguage']),
            'w'
    ) as f:
        f.writelines(POST_dict['code'])
    # with open(Config.codeSubmitStorePath+'/'+eId+'_code'+getCodeFileSuffix(POST_dict['codeLanguage']), 'w') as f:
    #     f.writelines(POST_dict['code'])

    # Docker preparation
    limitations = {
        'timeLimit': Problem.objects.get(problemId=rPId).timeLimit,
        'memoryLimit': Problem.objects.get(problemId=rPId).memoryLimit
    }

    dockerOutputFilePath = docker.PrepareDocker(eId, limitations)
    standardOutputFilePath = ''
    analyze.outputAnalyze(standardOutputFilePath, dockerOutputFilePath)









    return MyResponse.defaultRes


def getEvaluationList(request):
    """

    :param request:
    :return:
    """
    print(request)
    res = {}
    eva = Evaluation.objects.all()
    if request.method != 'GET':
        return MyResponse.methodWrongRes
    if ('currentPage' or 'pageSize') not in request.GET:
        return MyResponse.formEmptyRes
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))

    if 'relatedProblemId' in request.GET:
        eva = eva.filter(relatedProblemId=request.GET['relatedProblemId'])

    if 'author' in request.GET:
        eva = eva.filter(author=request.GET['author'])

    evaList = []
    for item in eva.values():
        evaList.append(item)
    evaList.reverse()

    totalNum = len(evaList)

    pageSize = int(request.GET['pageSize'])
    currentPage = int(request.GET['currentPage'])

    startSeq = min(pageSize * (currentPage - 1), totalNum)
    endSeq = min(pageSize * currentPage, totalNum)

    evaList = evaList[startSeq:endSeq]

    for item in evaList:
        for key in item:
            if key=='author_id':
                item['author'] = item[key]
                del item[key]
            elif key=='relatedProblemId_id':
                item['relatedProblemId'] = item[key]
                del item[key]
            elif key=='submitTime':
                item[key] = item[key].strftime('%Y-%m-%d %H:%M:%S')

    res['evaluationList'] = evaList
    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)
