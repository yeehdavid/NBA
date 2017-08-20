from django.shortcuts import render
from MainAPP.models import Videos, Board_News,Latest_News,Board_Videos,Lx,Lx_Part,Hoop_Latest_News
import collections
# Create your views here.
def index(request):
    B_N = Board_News.objects.all().order_by('-created_time')
    News_list0 = B_N[:1]#轮播的第一张
    News_list1 = B_N[1:5]#轮播的后面几张
    News_list2 = Latest_News.objects.all().order_by('-created_time')[0:11]
    Hoop_News = Hoop_Latest_News.objects.all().order_by('-created_time')[0:33]
    return render(request, 'index.html', context={'News_list0':News_list0,'News_list1':News_list1,'News_list2':News_list2,
                                                  'Hoop_left':Hoop_News[0:11],'Hoop_center':Hoop_News[11:22],'Hoop_right':Hoop_News[22:33]})

def videos(request):
    dic = collections.OrderedDict()
    luxiang=Lx.objects.all().order_by('created_time')[0:10]
    for l in luxiang:
        dic[l.title] = Lx_Part.objects.filter(Belong=l)


    return render(request,'videos.html',context={'luxiang':dic})


def ins(request):
    return render(request, 'haiwai/ins.html')

def mt(request):
    return render(request, 'haiwai/mt.html')

def pt(request):
    return render(request, 'haiwai/pt.html')

def go(request):
    return render(request, 'haiwai/go.html')