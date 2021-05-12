"""
django视图
"""
import random

from django.shortcuts import render

# Create your views here.

import os
from django.http import HttpResponse, JsonResponse, FileResponse, QueryDict
from HongyiOJ.models import *
from HongyiOJ.token import *
from HongyiOJ.utils import *
from HongyiOJ.config import *
import re

from django.core.mail import send_mail
from HongyiOJ_backend import settings

verifyDict = {}


def test(request):
    print(request)
    if request.method == 'GET':
        return HttpResponse('Welcome to Hongyi OJ!')
    else:
        return JsonResponse(methodWrongRes())


def login(request):
    """
    Login
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == 'POST':
        return JsonResponse(methodWrongRes())
    if not request.POST:
        return JsonResponse(formEmptyRes())

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
        return JsonResponse(methodWrongRes())
    if not request.POST:
        return JsonResponse(formEmptyRes())
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
        return JsonResponse(methodWrongRes())
    if 'email' not in request.GET:
        return JsonResponse(formEmptyRes())

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

    return JsonResponse(defaultRes())




def verify(request):
    """
    Verify
    :param request:
    :return:
    """
    print(request)
    res = {}
    if not request.method == "POST":
        return JsonResponse(methodWrongRes())
    if ('email' or 'verifyCode') not in request.POST:
        return JsonResponse(formEmptyRes())

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
    return JsonResponse(defaultRes())




def resetPassword(request):
    print(request)
    res = {}
    if not request.method == 'PUT':
        return JsonResponse(methodWrongRes())
    PUT = QueryDict(request.body)

    if 'email' not in PUT and 'password' not in PUT:
        return JsonResponse(formEmptyRes())

    if not User.objects.filter(email=PUT['email']).exists():
        res['isOk'] = False
        res['errMsg'] = '邮箱未绑定账户'
        return JsonResponse(res)

    User.objects.filter(email=PUT['email']).update(password=PUT['password'])

    return JsonResponse(defaultRes())


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
        return JsonResponse(methodWrongRes())

    PUT = QueryDict(request.body)
    if 'username' not in PUT:
        return JsonResponse(formEmptyRes())

    res['isOk'] = True
    res['errMsg'] = ''

    return JsonResponse(res)



def getProblemList(request):
    """
    Problem list
    :param request:
    GET {problemId|problemName, pageSize&currentPage, username}
    ps: currentPage starts with 1
    :return:
    problemList: Array
    resultSum: Int
    """
    print(request)
    res = {}
    problemDictArr = Problem.objects.all().values()
    if not request.method == 'GET':
        return JsonResponse(methodWrongRes())
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

    if 'reviewStatus' in request.GET:
        problems = Problem.objects.filter(reviewStatus=request.GET['reviewStatus'])
    else:
        problems = Problem.objects.all()

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
        return JsonResponse(formEmptyRes())

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

    for item in problemList:
        del item['stdProgram']
        del item['dataGenerator']

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
        return JsonResponse(methodWrongRes())
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))
    if not request.POST:
        return JsonResponse(formEmptyRes())
    POST_dict = request.POST.dict()
    seqNum = Problem.objects.count() + 1
    POST_dict['problemId'] = createProblemId(seqNum)
    POST_dict['reviewStatus'] = 'reviewing'

    Problem.objects.create(**POST_dict)

    return JsonResponse(defaultRes())


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
        return JsonResponse(methodWrongRes())
    if not isTokenAvailable(request) is None:
        return JsonResponse(isTokenAvailable(request))

    PUT = QueryDict(request.body)
    if ('problemId' or 'reviewStatus') not in PUT:
        return JsonResponse(formEmptyRes())
    Problem.objects.filter(problemId=PUT['problemId']).update(reviewStatus=PUT['reviewStatus'])

    return JsonResponse(defaultRes())



