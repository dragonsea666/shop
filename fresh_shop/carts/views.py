from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from carts.models import ShoppingCart
from goods.models import Goods


def cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        data = []
        if session_goods:
            for se_goods in session_goods:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                nums = se_goods[1]
                is_select = se_goods[2]
                price = goods.shop_price * se_goods[1]
                data.append([goods,nums, price,is_select])
        return render(request, './cart.html',{'goods_all': data})
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            session_goods = request.session.get('goods')
            data = []
            if session_goods:
                for se_goods in session_goods:
                    goods = Goods.objects.filter(pk=se_goods[0]).first()
                    nums = se_goods[1]
                    is_select = se_goods[2]
                    price = goods.shop_price * se_goods[1]
                    data.append([goods, nums, price, is_select])
            return render(request, './cart.html', {'goods_all': data})


def add_cart(request):
    if request.method == 'POST':
        #保存到session中
        #1.获取前端ajax提交的goode_id,num
        # 2.组装存储到session的数据
        goods_id = request.POST.get('goods_id')
        nums = request.POST.get('nums')
        # 组装存储的结构
        goods_list = [int(goods_id), int(nums), 1]
        #判断session中是否保存了goods
        session_goods = request.session.get('goods')
        if session_goods:
            # 添加或者修改
            flag = False
            for goods in session_goods:
                if goods[0] == int(goods_id):
                    goods[1] += int(nums)
                    flag = True
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            goods_count = len(session_goods)
        else:
            request.session['goods'] = [goods_list]
            goods_count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功','goods_count':goods_count})

def show_cart_count(request):
    if request.method == 'POST':
        try:
            session_goods = request.session.get('goods')
            goods_count = len(session_goods)
        except:
            goods_count = 0
        return JsonResponse({'code':200, 'msg':'请求成功','goods_count':goods_count})

def check_inventory(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)
        goods_nums = goods.goods_nums
        return JsonResponse({'code':200, 'msg':'请求成功','goods_nums':goods_nums})


def change_cart(request):
    if request.method == 'POST':

        goods_id = int(request.POST.get('goods_id'))
        is_select = request.POST.get('is_select')
        nums = request.POST.get('nums')
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods_id == goods[0]:
                goods[1] = int(nums) if nums else goods[1]
                if is_select:
                    is_selects = int(is_select)
                    goods[2] = is_selects
        request.session['goods'] = session_goods
        return JsonResponse({'code':200, 'msg':'请求成功'})

def del_cart(request,id):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(user_id=user_id,goods_id=id).delete()
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods[0] == int(id):
                session_goods.remove(goods)
        request.session['goods'] = session_goods
        return HttpResponseRedirect(reverse('carts:cart'))

def change_all_cart(request):
    if request.method == 'POST':
        is_select = request.POST.get('is_select')
        session_goods = request.session.get('goods')
        for goods in session_goods:
            goods[2] = int(is_select)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})