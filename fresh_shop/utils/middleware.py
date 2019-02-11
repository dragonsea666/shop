import re
import time
import logging

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from carts.models import ShoppingCart
from user.models import User


class LoginStatusMiddleware(MiddlewareMixin):

    def process_request(self, request):

        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        # if request.path == '/':
        #     return None
        not_need_path = ['/user/login/', '/media/','/user/register',
                         '/goods/','/carts/check_inventory/','/static/',
                         '/carts/cart/','/carts/add_cart/',
                         '/carts/show_cart_count/','/carts/change_cart/','/order/make_order/',]
        path = request.path
        for not_path in not_need_path:
            # 匹配当前路径是否为不需要登录验证的路径
            if re.match(not_path, path):
                return None
        # 当前的请求url不在not_need_path中，则表示当前url需要登录才能访问

        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                request.user = user
                return None
            except:
                return HttpResponseRedirect('/user/login/')
        else:
            return HttpResponseRedirect('/user/login/')

    def process_response(self, request, response):

        return response


log = logging.getLogger(__name__)


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 绑定在request上的一个属性
        request.init_time = time.time()

    def process_response(self, request, response):
        # 请求时间
        count_time = time.time() - request.init_time
        # 请求状态码
        code = response.status_code
        # 请求地址
        path = request.path
        # 请求方法
        method = request.method
        # 响应内容
        try:
            content = response.content
        except:
            content = response.streaming_content
        log_str = '%s %s %s %s %s' % (count_time, code, path, method, content)
        log.info(log_str)
        return response

class SessionSyncMiddleware(MiddlewareMixin):


    def process_response(self, request,response):

        user_id = request.session.get('user_id')
        if user_id:
            session_goods = request.session.get('goods')
            if session_goods:
                # 判断session数据是否存在数据库中
                shop_carts = ShoppingCart.objects.filter(user_id=user_id)
                data = []
                # 标识符flag，修改了商品信息
                for goods in shop_carts:
                    for se_goods in session_goods:
                        if se_goods[0] == goods.goods_id:
                            goods.nums = se_goods[1]
                            goods.is_select = se_goods[2]
                            goods.save()
                            # 向data中添加更新了的商品
                            data.append(se_goods[0])
                session_goods_ids = [i[0] for i in session_goods]
                add_goods_ids = list(set(session_goods_ids) - set(data))
                for add_goods_id in add_goods_ids:
                    for session_good in session_goods:
                        if add_goods_id == session_good[0]:
                            ShoppingCart.objects.create(user_id=user_id,goods_id=add_goods_id,nums=session_good[1])
            # 将数据库数据同步到session中
            new_shop_carts = ShoppingCart.objects.filter(user_id=user_id)
            session_new_goods = [[i.goods_id,i.nums,i.is_select] for i in new_shop_carts]
            request.session['goods'] = session_new_goods
        return response