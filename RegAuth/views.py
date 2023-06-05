from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from .forms import Authentication, Registration
from booking.models import User

from django.urls import reverse
from urllib.parse import urlencode

# Create your views here.


def auth(request):
    if request.method == 'POST':
        if User.objects.filter(login=request.POST['login'], password=request.POST['passwd']).exists():
            userid = User.objects.filter(login=request.POST['login'], password=request.POST['passwd'])[0].pk

            base_url = reverse('home')
            query_str = urlencode({'userid': userid})
            url = '{}?{}'.format(base_url, query_str)
            return redirect(url) ######адрес страницы ++++ учитывать пользователя ++++ для модели необходимо выводить IdUser(см. выше)
        else:
            error_msg = "Несуществующий пользователь"
            form = Authentication(request.POST)
            form.add_error(None, error_msg)
    else:
        form = Authentication()
    return render(request, "RegAuth/authorization.html", {"form": form})


def reg(request):
    if request.method == 'POST':
        if User.objects.filter(login=request.POST['login'], password=request.POST['passwd']).exists():
            error_msg = "Такой пользователь уже существует"
        else:
            if request.POST['passwd'] == request.POST['passwd_check']:
                User.objects.create(email=request.POST['email'], password=request.POST['passwd'],
                                    login=request.POST['login'], role="Пользователь")
                return redirect('authentication')
            else:
                error_msg = "Пароли не совпадают"
        form = Registration(request.POST)
        form.add_error(None, error_msg)
    else:
        form = Registration()
    return render(request, "RegAuth/registration.html", {"form": form})
