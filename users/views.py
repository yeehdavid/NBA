from django.shortcuts import render, redirect
from .forms import RegisterForm
from MainAPP.models import Videos, Board_News,Latest_News,Board_Videos
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()
    return render(request,'users/register.html',context={'form':form})
# Create your views here.

def index(request):
    B_N = Board_News.objects.all().order_by('created_time')
    News_list0 = B_N[:1]#轮播的第一张
    News_list1 = B_N[1:5]#轮播的后面几张
    News_list2 = Latest_News.objects.all().order_by('created_time')[0:10]
    return render(request, 'index.html', context={'News_list0':News_list0,'News_list1':News_list1,'News_list2':News_list2})