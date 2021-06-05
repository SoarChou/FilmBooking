from django.shortcuts import render,redirect
from . import models
from .forms import LoginForm, UserForm
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    nav_login = '''
          <li class="nav-item left">
            <a class="nav-link" href="/login/">登录</a>
          </li>
          <li class="nav-item left">
            <a class="nav-link" href="/register/">注册</a>
          </li>
    '''
    if request.session.get('is_login',None):
        username = request.session['user_name']
        # <li class="nav-item dropdown">
        #   <a class="nav-link dropdown-toggle" href="#" id="navbardrop" data-toggle="dropdown">
        #     Dropdown link
        #   </a>
        #   <div class="dropdown-menu">
        #     <a class="dropdown-item" href="#">Link 1</a>
        #     <a class="dropdown-item" href="#">Link 2</a>
        #     <a class="dropdown-item" href="#">Link 3</a>
        #   </div>
        # </li>
        nav_login = '<li class="nav-item dropdown left"><a class="nav-link dropdown-toggle" href="#" id="navbardrop" data-toggle="dropdown">' + username + '</a>'+ '''
            <div class="dropdown-menu">
             <a class="dropdown-item" href="/logout/" style="font-size:8px;"><i class="fas fa-sign-out fa-2x"></i> &nbsp登出</a>
             <a class="dropdown-item" href="/changeuser/" style="font-size:8px;">
                <span class="fa-layers fa-fw fa-2x">
                    
                    <i class="fas fa-user" data-fa-transform="left-2"></i>
                    <i class="fas fa-exchange-alt" data-fa-transform="shrink-10 down-4 right-1" style="color:white"></i>
                </span>
                 切换
             </a>
            </div>
          </li>
          <li class="nav-item">
            
          <li>
        '''
    else:
        pass
    
    movies = models.Movie.objects.all()
    # 分页，每页18个电影
    movie_pages = Paginator(movies,18)
    if movie_pages.num_pages <= 1:
        movie_list = movies
        data = ""
    else:
        page = int(request.GET.get('page',1))
        movie_list = movie_pages.page(page)
        left = []
        right = []
        left = []  # 当前页左边连续的页码号，初始值为空
        right = []  # 当前页右边连续的页码号，初始值为空
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False   # 标示是否需要显示第 1 页的页码号
        last = False  # 标示是否需要显示最后一页的页码号
        total_pages = movie_pages.num_pages  
        page_range = movie_pages.page_range 
        if page == 1:  #如果请求第1页
            right = page_range[page:page+2]  #获取右边连续号码页
            print(total_pages)
            if right[-1] < total_pages - 1:    # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
                right_has_more = True
            if right[-1] < total_pages:   # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
                last = True
        elif page == total_pages:  #如果请求最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]  #获取左边连续号码页
            if left[0] > 2:
                left_has_more = True  #如果最左边的号码比2还要大，说明其与第一页之间还有其他页码，因此需要显示省略号，通过 left_has_more 来指示
            if left[0] > 1: #如果最左边的页码比1要大，则要显示第一页，否则第一页已经被包含在其中
                first = True
        else:  #如果请求的页码既不是第一页也不是最后一页
            left = page_range[(page-3) if (page-3) > 0 else 0:page-1]   #获取左边连续号码页
            right = page_range[page:page+2] #获取右边连续号码页
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last,
            'total_pages':total_pages,
            'page':page
        }
    return render(request,'index.html', locals())
 
def login(request):
    # 检测session登录信息，避免重复登陆
    if request.session.get('is_login',None):
        return redirect('/index')

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        # locals()函数传回所有本地变量字典
        return render(request, 'login/login.html',  locals())
    
    login_form = LoginForm()
    return render(request, 'login/login.html', locals())
 
def register(request):
    # 不允许已登录用户进入注册
    if request.session.get('is_login',None):
        return redirect('/index')
    
    if request.method == "POST":
        register_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        erro=0 # 判断是否有错
        if register_form.is_valid():  # 确保用户名和密码都不为空
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password_repeat = register_form.cleaned_data['password_repeat']
            email = register_form.cleaned_data['email']
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(name=username)
                msg_name = "已有该用户名"
                erro = 1
            except:
                pass

            try:
                email = models.User.objects.get(email=email)
                msg_email = "已有该邮箱"
                erro = 1
            except:
                pass

            if password_repeat != password:
                msg_password2 = "两次密码不相同"
                erro = 1
        
            # 有错误信息，返回错误信息
            if erro:
                return render(request, 'login/register.html',  locals())
            else:
                NewUser = models.User()
                NewUser.name =  username
                NewUser.password = password
                NewUser.email = email
                NewUser.sex = request.POST.get('gender')
                NewUser.save()
                return redirect('/success/')

        else:
            pass
        # msg_email
        # msg_password
        # msg_password2
    register_form = UserForm()
    return render(request,'login/register.html', locals())
 
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
        # 清除session
    request.session.flush()
    return redirect('/index/')

def change_user(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect('/login/')

def success(request):
    pass
    return render(request, 'login/success.html')

def movie(request,movie_id):
    pass
    return render(request, 'login/success.html')