from django.shortcuts import render
from MainAPP.models import Videos, Board_News,Latest_News,Board_Videos,Lx,Lx_Part

# Create your views here.
def index(request):
    B_N = Board_News.objects.all().order_by('-created_time')
    News_list0 = B_N[:1]#轮播的第一张
    News_list1 = B_N[1:5]#轮播的后面几张
    News_list2 = Latest_News.objects.all().order_by('-created_time')[0:10]
    return render(request, 'index.html', context={'News_list0':News_list0,'News_list1':News_list1,'News_list2':News_list2})

def videos(request):
    dic = dict()
    luxiang=Lx.objects.all().order_by('-created_time')[0:10]
    for l in luxiang:
        dic[l.title] = Lx_Part.objects.filter(Belong=l)


    return render(request,'videos.html',context={'luxiang':dic})