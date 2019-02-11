from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from carts.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.functions import get_order_sn


def place_order(request):
    if request.method == 'GET':
        # 从数据库取数据
        user_id = request.session.get('user_id')
        shop_carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1)
        if shop_carts:
            all_total = 0
            for carts in shop_carts:
                price = carts.nums * carts.goods.shop_price
                carts.total = price
                all_total += price
            carts_count = len(shop_carts)
            user_id = request.session.get('user_id')
            site_info = UserAddress.objects.filter(user_id=user_id)
            return render(request,'./place_order.html', {'shop_carts':shop_carts, 'site_info':site_info,
                                                         'all_total': all_total,'carts_count':carts_count})
        else:
            return render(request, './cart.html')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            if request.method == 'GET':
                # 从数据库取数据
                user_id = request.session.get('user_id')
                shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)
                if shop_carts:
                    all_total = 0
                    for carts in shop_carts:
                        price = carts.nums * carts.goods.shop_price
                        carts.total = price
                        all_total += price
                    carts_count = len(shop_carts)
                    user_id = request.session.get('user_id')
                    site_info = UserAddress.objects.filter(user_id=user_id)
                    return render(request, './place_order.html', {'shop_carts': shop_carts, 'site_info': site_info,
                                                                  'all_total': all_total, 'carts_count': carts_count})
                else:
                    return render(request, './cart.html')


def user_center_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        page = request.GET.get('page',1)
        order_info = OrderInfo.objects.filter(user_id=user_id)
        paginator =Paginator(order_info,5)
        page = paginator.page(page)
        return render(request,'./user_center_order.html',{'page': page})
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            user_id = request.session.get('user_id')
            page = request.GET.get('page', 1)
            order_info = OrderInfo.objects.filter(user_id=user_id)
            paginator = Paginator(order_info, 5)
            page = paginator.page(page)
            return render(request, './user_center_order.html', {'page': page})

def make_order(request):
    if request.method == 'POST':
        #创建订单
        #创建订单详情和购物车删除已下单的商品
        user_id = request.session['user_id']
        shop_carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1)
        order_mount = 0
        for carts in shop_carts:
            order_mount += carts.nums * carts.goods.shop_price
        order_sn = get_order_sn()
        address_id = request.POST.get('address_id')
        user_address = UserAddress.objects.filter(pk=address_id).first()
        order = OrderInfo.objects.create(user_id=user_id,order_sn=order_sn,order_mount=order_mount,
                                         address=user_address.address,signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile,
                                         )
        for carts in shop_carts:
            OrderGoods.objects.create(order=order,goods=carts.goods,goods_nums=carts.nums)
        shop_carts.delete()
        request.session.pop('goods')
        return JsonResponse({'code':200,'msg':'请求成功'})


