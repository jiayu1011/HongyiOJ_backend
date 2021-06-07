"""
Standard Json response
"""
from django.http import HttpResponse, JsonResponse
class MyResponse:
    defaultRes = JsonResponse({
            'isOk': True,
            'errMsg': '',
        })
    methodWrongRes = JsonResponse({
            'isOk': False,
            'errMsg': '请求方法错误'
        })
    formEmptyRes = JsonResponse({
            'isOk': False,
            'errMsg': '表单内容为空'
        })




