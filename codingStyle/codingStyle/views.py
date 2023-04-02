from django.http import HttpResponse
from django.shortcuts import render


def checkStyle(request):
    if request.method == 'GET':
        return render(request, 'main.html')
    elif request.method == 'POST':
        code = request.POST['code']
        return render(request, 'main.html', locals())
