"""
django视图
"""

from django.shortcuts import render

# Create your views here.

import os
from django.http import HttpResponse, JsonResponse, FileResponse
from HongyiOJ.models import *
from HongyiOJ.token import *
from HongyiOJ.utils import *
from HongyiOJ.config import *
import re





def test(request):
    print(request)
    if request.method == 'GET':
        return HttpResponse('Welcome to Hongyi OJ!')
    else:
        return JsonResponse(methodWrongRes())


def login(request):
    print(request)
    res = {}
    if request.method == 'POST':
        if request.POST:
            print(request.POST)
            if not User.objects.filter(username=request.POST['username']).exists():
                res['isOk'] = False
                res['errMsg'] = '用户不存在'
            else:
                tempUserDict = User.objects.get(username=request.POST['username'])
                if request.POST['password'] != tempUserDict.password:
                    res['isOk'] = False
                    res['errMsg'] = '密码错误'

                else:
                    token = createToken(request.POST['username'])

                    res['userInfo'] = User.objects.filter(username=request.POST['username']).values()[0]
                    res['token'] = token
                    res['isOk'] = True
                    res['errMsg'] = ''

            return JsonResponse(res)

        else:
            return JsonResponse(formEmptyRes())
    else:
        return JsonResponse(methodWrongRes())



def register(request):
    print(request)
    res = {}
    if request.method == 'POST':
        if request.POST:
            print(request.POST)
            POST_dict = request.POST.dict()

            if User.objects.filter(username=POST_dict['username']).exists():
                res['isOk'] = False
                res['errMsg'] = '用户名已经存在'

            else:
                if POST_dict['username'] == 'admin':
                    POST_dict['identity'] = 'admin'
                User.objects.create(**POST_dict)

                res['userInfo'] = POST_dict
                res['isOk'] = True
                res['errMsg'] = ''

            return JsonResponse(res)
        else:
            return JsonResponse(formEmptyRes())
    else:
        return JsonResponse(methodWrongRes())


def logout(request):
    """
    :param request:
    :return:
    """
    print(request)
    res = {}
    if request.method == 'PUT':

        res['isOk'] = True
        res['errMsg'] = ''


        return JsonResponse(res)
    else:
        return JsonResponse(methodWrongRes())



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
    problems = Problem.objects.all().values()
    if request.method == 'GET':
        # If user has logged in, validate his token
        if 'HTTP_AUTHORIZATION' in request.META:
            clientToken = request.META['HTTP_AUTHORIZATION']
            payload, msg = validateToken(clientToken)
            if msg is not None:
                res['isOk'] = False
                res['errMsg'] = msg
                return JsonResponse(res)

        problemList = []
        targetProblems = []
        doneList = []
        resultSum = 0

        if 'username' in request.GET:
            doneList = User.objects.get(username=request.GET['username']).acProblems.split(',')

        if 'problemId' in request.GET:
            problemList.append(Problem.objects.filter(problemId=request.GET['problemId']).values()[0])
            resultSum = 1

        elif 'problemName' in request.GET:
            problemName = request.GET['problemName']
            names = []
            conditions = {}
            for item in problems:
                regExp = r'.*' + problemName + r'.*'
                # 正则匹配， re.I表示不区分大小写
                if re.search(regExp, item['name'], re.I) is not None:
                    name = re.search(regExp, item['name'], re.I).group()
                    names.append(name)

            for name in names:
                cds = conditions
                cds['problemName'] = name

                targetProblems.append(Problem.objects.filter(**cds).values()[0])

        if 'pageSize' in request.GET and 'currentPage' in request.GET:
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
                resultSum = Problem.objects.count()
                pageSize = int(request.GET['pageSize'])
                currentPage = int(request.GET['currentPage'])

                startSeq = min(pageSize*(currentPage-1), resultSum)
                endSeq = min(pageSize*currentPage, resultSum)

                for i in range(startSeq, endSeq):
                    item = problems[i]
                    if 'username' not in request.GET:
                        item['isDone'] = False
                    else:
                        item['isDone'] = item['problemId'] in doneList

                    problemList.append(item)



        res['problemList'] = problemList
        res['resultSum'] = resultSum
        res['isOk'] = True
        res['errMsg'] = ''

        return JsonResponse(res)
    else:
        return JsonResponse(methodWrongRes())


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
    if request.method == 'POST':
        if request.POST:
            POST_dict = request.POST.dict()
            seqNum = Problem.objects.count() + 1
            POST_dict['problemId'] = createProblemId(seqNum)


            Problem.objects.create(**POST_dict)
            res['isOk'] = True
            res['errMsg'] = ''
            return JsonResponse(res)
        else:
            return JsonResponse(formEmptyRes())
    else:
        return JsonResponse(methodWrongRes())

