from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect


# Create your views here.
# 学生信息列表处理函数
def index(request):

    return render(request, 'admin/index.html')