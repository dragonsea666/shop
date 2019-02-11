from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from goods.models import Goods, GoodsCategory

from user.models import User
# from rest_framework import mixins, viewsets
from django.urls import reverse
# from goods.goodserializer import GoodSerializer

# class Goodview(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin,
#              mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,):
#     queryset = Goods.objects.all()
#     serializer_class = GoodSerializer
#     # 过滤
#     # filter_class = ArticleFilter
#
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data)
#         except:
#             data = {}
#             data['code'] = 500
#             data['msg'] = '获取数据失败'
#             return Response(data)


def index(request):
    if request.method == 'GET':
        data = {}

        for cate in GoodsCategory.CATEGORY_TYPE:
            goods = Goods.objects.filter(category_id=cate[0])[0:4]
            data[cate[1]] = goods
        return render(request, './index.html', {'goods_category': data})

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            data = {}
            for cate in GoodsCategory.CATEGORY_TYPE:
                goods = Goods.objects.filter(category_id=cate[0])[0:4]
                data[cate[1]] = goods
            return render(request, './index.html', {'goods_category': data})




def detail(request, id):

    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        try:
            goods.goods_desc = goods.goods_desc.replace('\\n', '').replace('\\', '').replace('data-lazyload', 'src')
        except:
            pass
        data = {}
        for cate in GoodsCategory.CATEGORY_TYPE:
            data[cate[1]] = cate[0]
        return render(request, './detail.html', {'goods': goods,'data':data})

    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list')+'?keyword={}'.format(keyword))
        else:
            goods = Goods.objects.filter(pk=id).first()
            try:
                goods.goods_desc = goods.goods_desc.replace('\\n', '').replace('\\', '').replace('data-lazyload', 'src')
            except:
                pass
            data = {}
            for cate in GoodsCategory.CATEGORY_TYPE:
                data[cate[1]] = cate[0]
            return render(request, './detail.html', {'goods': goods, 'data': data})


def list(request, category_id):

    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        goods = Goods.objects.filter(category_id=category_id)
        paginator = Paginator(goods, 15)
        page = paginator.page(page)
        data = {}
        for cate in GoodsCategory.CATEGORY_TYPE:
            data[cate[1]] = cate[0]
        return render(request, './list.html',{'page':page, 'category_id':category_id,'data':data})
    else:
        keyword = request.POST.get('keyword')
        if keyword:
            return HttpResponseRedirect(reverse('goods:search_list') + '?keyword={}'.format(keyword))
        else:
            page = int(request.GET.get('page', 1))
            goods = Goods.objects.filter(category_id=category_id)
            paginator = Paginator(goods, 15)
            page = paginator.page(page)
            data = {}
            for cate in GoodsCategory.CATEGORY_TYPE:
                data[cate[1]] = cate[0]
            return render(request, './list.html', {'page': page, 'category_id': category_id, 'data': data})



def search_list(request):

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        keyword = request.GET.get('keyword')
        goods = Goods.objects.filter(name__icontains=keyword)
        paginator = Paginator(goods, 15)
        page = paginator.page(page)

        return render(request,'./search_list.html',{'page':page,'keyword':keyword})
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        if keyword:
            page = request.GET.get('page', 1)
            goods = Goods.objects.filter(name__icontains=keyword)
            paginator = Paginator(goods, 15)
            page = paginator.page(page)
            return render(request, './search_list.html', {'page': page, 'keyword': keyword})
        else:
            return render(request, './search_list.html')

    # if request.method == 'POST':
    #     keyword = request.POST.get('keyword')
    #     page = int(request.POST.get('page',1))
    #     goods = Goods.objects.filter(name__icontains=keyword)
    #     paginator = Paginator(goods,15)
    #     page = paginator.page(page)
    #
