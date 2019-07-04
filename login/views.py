from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from login.models import User


def login(request):
    '''显示登录页面'''

    # 判断用户是否已经登录
    # 获取session
    if request.session.has_key('islogin'):
        return redirect('/main')
    else:
        # 获取cookie保存的username
        if 'username' in request.COOKIES:
            # 获取cookie
            username = request.COOKIES['username']
        else:
            username = ''

        return render(request, 'login/login.html', {'username': username})


def login_check(request):
    '''登录校验'''
    query_dict = request.POST
    username = query_dict.get('username')
    password = query_dict.get('password')
    remember = query_dict.get('remember')

    print(username + remember)

    # 从数据库查询
    user = User.objects.filter(Q(username__exact=username) & Q(password__exact=password))

    if user:
        # 登录成功
        response = JsonResponse({'res': '1'})

        # 判断是否需要记住用户名
        if remember == 'true':
            # 设置cookie
            response.set_cookie('username', username, max_age=7 * 24 * 3600)

        # 记住用户的登录状态
        # 设置session
        request.session['islogin'] = True
        # 记住登录用户的用户名
        request.session['username'] = username

        request.session.set_expiry(7 * 24 * 3600)

        return response

    else:
        # 登录失败
        return JsonResponse({'res': '0'})


def main(request):
    '''登录成功后，显示登录主页面'''
    return render(request, 'login/main.html')


def ajax_test(request):
    '''显示ajax页面'''
    return render(request, 'login/ajax_test.html')


def ajax_handler(request):
    '''处理ajax请求'''
    return JsonResponse({'res': '1'})


# ---------------------CSRF跨域请求伪造----------------------------
def login_required(function):
    '''检验必须登录的装饰器'''

    def wapper(request, *args, **kwargs):
        if request.session.has_key('islogin'):
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('login:login'))

    return wapper


@login_required
def change_pwd(request):
    '''显示修改密码页面'''
    return render(request, 'login/change_pwd.html')


@login_required
def handler_change_pwd(request):
    '''处理修改密码逻辑'''
    # 获取新密码
    query_dict = request.POST
    pwd = query_dict.get('pwd')

    # 从session中获取用户名
    username = request.session.get('username')
    return JsonResponse({'res': '1'})

    # 修改数据库中该用户的密码
    # user = User.objects.get(username=username)
    # if user:
    #     user.password = pwd
    #     user.save()
    #     return JsonResponse({'res': '1'})
    # else:
    #     return JsonResponse({'res': '0'})
