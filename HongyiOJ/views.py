"""
django视图
"""

from django.shortcuts import render

# Create your views here.

import os
from django.http import HttpResponse,JsonResponse,FileResponse

from HongyiOJ.models import *

from HongyiOJ.token import *





defaultRes = {
    'isOk': True,
    'errMsg': '',
}


def test(request):
    print(request)
    if request.method == 'GET':
        return HttpResponse('Welcome to Hongyi OJ!')


def login(request):
    print(request)
    res = defaultRes
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

            return JsonResponse(res)



def register(request):
    print(request)
    res = defaultRes
    if request.method == 'POST':
        if request.POST:
            print(request.POST)

            if User.objects.filter(username=request.POST['username']).exists():
                res['isOk'] = False
                res['errMsg'] = '用户名已经存在'

            else:
                User.objects.create(
                    username=request.POST['username'],
                    password=request.POST['password'],
                    email=request.POST['email']
                )


                res['userInfo'] = request.POST.dict()

            return JsonResponse(res)


def logout(request):
    print(request)
    if request.method == 'GET':


        return JsonResponse(defaultRes)
