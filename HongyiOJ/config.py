"""
Standard Json response key
"""
def defaultRes():
    return {
        'isOk': True,
        'errMsg': '',
    }

def methodWrongRes():
    return {
        'isOk': False,
        'errMsg': '请求方法错误'
    }

def formEmptyRes():
    return {
        'isOk': False,
        'errMsg': '表单内容为空'
    }

