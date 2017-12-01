from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
from sign.models import Event, Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

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

    event_list = Event.objects.all()

    # session
    username = request.session.get('user','') # 读取浏览器session

    return render(request,'event_manage.html',{'user':username,'events':event_list})

@login_required
def search_name(request):
    '发布会名称搜索'

    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user',)
    guest_list = Guest.objects.all()

    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer,deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of rang(e.g. 9999),deliver last page of result.
        contacts = paginator.page(paginator.num_pages)

    return render(request,'guest_manage.html',{'user':username,'guests':contacts})


@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    return render(request,'sign_index.html',{'event':event})

@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id = event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)

    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error!'})

    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone or event_id error!'})

    result = Guest.objects.get(phone=phone,event_id=event_id)
    print(result.sign)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in !'})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})

@login_required
def logout(request):
    auth.logout(request) # 退出登录
    response = HttpResponseRedirect('/index/')
    return response
