import time
from urllib.request import Request

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpRequest
from .models import User
from .forms import Login

token_detail = {}
add_user_token = []


def get_token(request):
    token = request.COOKIES.get('token')
    if token is None or token_detail.get(token) is None:
        print("Enter")
        # HttpResponseRedirect("/login/")
        redirect("http://192.168.1.7:8000/login/")
    return token


def generate_uid():
    return str(time.time_ns())


def login(request):
    form = Login()
    return render(request, './old-index.html', {'form': form})


def home(request):
    if request.method == 'POST':
        login_form = Login(request.POST)
        if login_form.is_valid():
            print("Form data", login_form.cleaned_data)
            user_id = login_form.cleaned_data['user_id']
            password = login_form.cleaned_data['password']

            user = User.objects.filter(user_id=user_id, password=password).first()

            if user is None or user.user_id is None:
                return login(request)
        uid = generate_uid()

        token_detail[uid] = {"type": user.user_type, "user_id": user.user_id}
        res_data = {}
        if user.user_type == 3:
            res_data['normal'] = True
            res_data['gov'] = False
        else:
            res_data['gov'] = True
            res_data['normal'] = False
        res = render(request, "index.html", res_data)
        res.set_cookie('token', uid, path='/')
        return res
    else:
        return login(request)
    token = request.COOKIES.get('token')
    if token is None or token_detail.get(token) is None:
        return login(request)
    res_data = {}
    user_type = token_detail[token].get('type')
    if user_type == 3:
        res_data['normal'] = True
        res_data['gov'] = False
    else:
        res_data['gov'] = True
        res_data['normal'] = False

    return render(request, "index.html",  data)


def add_user(request):
    token = request.COOKIES.get('token')
    return render(request, "add-user.html")


def add_voter(request):
    token = request.COOKIES.get('token')
    return render(request, "add-voter.html")


def contract(request):
    return render(request, "contract.html")


def get_vote_count(request):
    return render(request, "get-vote-count.html")


def vote(request):
    return render(request, "vote.html")
