from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):

    # return HttpResponse('Hello Django!')
    return render(request,'index.html')

# 登录管理
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username,password = password)
        # if username == 'admin' and password == 'admin123':
        if user is not None:
            auth.login(request,user) # 登录
            #return  HttpResponse('login success!')
            #return HttpResponseRedirect('/event_manage/')
            # response = HttpResponseRedirect('/event_manage/')
            # cookie
            # response.set_cookie('user',username,3600) # 添加浏览器cookie, 时长3600秒

            # session
            request.session['user'] = username # 将 session 信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return  response

        else:
            return render(request,'index.html',{'error':'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    #return render(request,'event_manage.html')
    # cookie
    #username = request.COOKIES.get('user','') # 读取cookie 默认为空

    # session
    username = request.session.get('user','') # 读取浏览器session

    return render(request,'event_manage.html',{'user':username})