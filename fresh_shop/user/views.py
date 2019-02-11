from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.hashers import check_password,make_password
# Create your views here.
from user.forms import UserRegisterForm, UserLoginForm, UserSiteForm
from user.models import User, UserAddress
from django.urls import reverse


def login(request):
    if request.method == 'GET':

        return render(request, './login.html')

    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd']
            user = User.objects.filter(username=username).first()
            if check_password(pwd,user.password):
                request.session['user_id'] = user.id

                return HttpResponseRedirect(reverse('goods:index'))

            else:
                err_pwd = '账号或密码错误'
                return render(request,'./login.html', {'err_pwd':err_pwd})
        else:
            errors = form.errors
            return render(request, './login.html', {'errors':errors})


def register(request):
    if request.method == 'GET':

        return render(request, './register.html')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['email']
            new_password = make_password(password)
            User.objects.create(username=username,password=new_password, email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            errors = form.errors
            return render(request,'./register.html',{'errors': errors})

def user_center_info(request):
    if request.method == 'GET':

        return render(request, './user_center_info.html')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            return render(request, './user_center_info.html')

def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        site_info = UserAddress.objects.filter(user_id=user_id)
        return render(request,'./user_center_site.html', {'site_info':site_info})
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            user_id = request.session.get('user_id')
            site_info = UserAddress.objects.filter(user_id=user_id)
            return render(request, './user_center_site.html', {'site_info': site_info})

    if request.method == 'POST':
        form = UserSiteForm(request.POST)
        if form.is_valid():
            signer_name = form.cleaned_data['signer_name']
            site = form.cleaned_data['site']
            postcode = form.cleaned_data['postcode']
            phone = form.cleaned_data['phone']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(signer_name=signer_name,address=site,signer_postcode=postcode,signer_mobile=phone,user_id=user_id)
            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            errors = form.errors
            return render(request, './user_center_site.html', {'errors': errors})






