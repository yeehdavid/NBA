from django.shortcuts import render
from MainAPP.models import Videos, Board_News, Latest_News, Board_Videos, Lx, Lx_Part, Hoop_Latest_News, Jrs, \
    ZiMeiTi_Article
import collections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    B_N = Board_News.objects.all().order_by('-created_time')
    News_list0 = B_N[:1]  # 轮播的第一张
    News_list1 = B_N[1:5]  # 轮播的后面几张
    News_list2 = Latest_News.objects.all().order_by('-created_time')[0:9]
    Hoop_News = Hoop_Latest_News.objects.all().order_by('-created_time')[0:33]

    return render(request, 'index.html',
                  context={'News_list0': News_list0, 'News_list1': News_list1, 'News_list2': News_list2,
                           'Hoop_left': Hoop_News[0:11], 'Hoop_center': Hoop_News[11:22],
                           'Hoop_right': Hoop_News[22:33]

                           })


def videos(request):
    dic = collections.OrderedDict()
    luxiang = Lx.objects.all().order_by('-created_time')[0:15]
    for l in luxiang:
        dic[l.title] = Lx_Part.objects.filter(Belong=l)
    jrs_list = Jrs.objects.all().order_by('created_time')

    return render(request, 'videos.html', context={'luxiang': dic, 'jrs_list': jrs_list})


def zhibo(request):
    jrs_list = Jrs.objects.all().order_by('created_time')
    return render(request, 'zhibo.html', context={'jrs_list': jrs_list})


def ins(request):
    return render(request, 'haiwai/ins.html')


def mt(request):
    return render(request, 'haiwai/mt.html')


def pt(request):
    return render(request, 'haiwai/pt.html')


def go(request):
    return render(request, 'haiwai/go.html')


def zimeiti(request):
    Article = ZiMeiTi_Article.objects.all().order_by('-created_time')
    # Article = list(range(100))
    paginator = Paginator(Article, 5)  # 实例化一个分页对象

    page = request.GET.get('page')  # 获取页码

    try:
        articles = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        articles = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        articles = paginator.page(paginator.num_pages)  # 取最后一页的记录


    return render(request, 'zimeiti.html', context={'article_list': articles})
