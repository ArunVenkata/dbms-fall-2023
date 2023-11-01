from django.shortcuts import render
from django.db import connection

def runoob(request):
    context = {}
    # context['hello'] = 'Hello World!'
    # return render(request, 'runoob.html', context)

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM course")
        results = cursor.fetchall()
        results= results[0]
        a = results[0]
        context['b'] = a
    #context['hello'] = results[0]
    return render(request, 'runoob.html', context)