from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
# 学生信息列表处理函数
def choose(request):

    return render(request, 'login/choose.html')

def login(request):
    return render(request, 'login/login.html')
    # if request.method == 'POST':
    #     #form = MyForm(request.POST)
    #     username = request.POST.get('username', 'username')
    #     password = request.POST.get('password', 'password')
    # print(username)
    # print(password)

# def get_data(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', 'username')
#         password = request.POST.get('password', 'password')
#         print(username)
#         print(password)
#         return render(request, 'admin/index.html')
# 表单
def search_form(request):
    return render(request, 'search_form.html')

def search(request):
    request.encoding='utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)


