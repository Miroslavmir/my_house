from django.shortcuts import render
from django.http import HttpResponse



def index(request):

    context = {
        'title': 'Home',
        'content': 'Добро пожаловать на наш сайт',

    }


    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('Home pAGE about')



