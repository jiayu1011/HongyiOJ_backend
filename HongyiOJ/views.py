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




# 样例标准返回必带字段
defaultRes = {
    'isOk': True,
    'errMsg': '',
}
methodWrongRes = {
    'isOk': False,
    'errMsg': '请求方法错误'
}
formEmptyRes = {
    'isOk': False,
    'errMsg': '表单内容为空'
}


def test(request):
    print(request)
    if request.method == 'GET':
        return HttpResponse('Welcome to Hongyi OJ!')
    else:
        return JsonResponse(methodWrongRes)


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
            return JsonResponse(formEmptyRes)
    else:
        return JsonResponse(methodWrongRes)



def register(request):
    print(request)
    res = {}
    if request.method == 'POST':
        if request.POST:
            print(request.POST)
            POST_dict = request.POST.dict()

            if User.objects.filter(username=request.POST['username']).exists():
                res['isOk'] = False
                res['errMsg'] = '用户名已经存在'

            else:
                User.objects.create(**POST_dict)
                # User.objects.create(
                #     username=request.POST['username'],
                #     password=request.POST['password'],
                #     email=request.POST['email']
                # )


                res['userInfo'] = request.POST.dict()
                res['isOk'] = True
                res['errMsg'] = ''

            return JsonResponse(res)
        else:
            return JsonResponse(formEmptyRes)
    else:
        return JsonResponse(methodWrongRes)


def logout(request):
    print(request)
    res = {}
    if request.method == 'PUT':

        res['isOk'] = True
        res['errMsg'] = ''


        return JsonResponse(res)
    else:
        return JsonResponse(methodWrongRes)


def getProblemList(request):
    # TODO: Not yet implemented
    print(request)
    res = {}
    if request.method == 'GET':


        return JsonResponse(res)
    else:
        return JsonResponse(methodWrongRes)


def uploadProblem(request):
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
            return JsonResponse(formEmptyRes)
    else:
        return JsonResponse(methodWrongRes)

