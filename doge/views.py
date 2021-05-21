from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
import requests
import time
from bs4 import BeautifulSoup
from django.urls import reverse
import validators
import datetime
import random
import string
import json
from .models import User, Link, Click

# Create your views here.

version = 1.4  # prototype


@csrf_exempt
def index(request):
    if request.user.is_authenticated != True:
        if request.method == "POST":
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "landing.html",
                              {"message": "Invalid username and/or password."})
        return render(request, "landing.html")
    else:
        return HttpResponseRedirect(reverse("dashboard"))


@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = ""

        # Ensure password matches confirmation
        password = request.POST["password"]

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html",
                          {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def create(request):
    if request.user.is_authenticated != True:
        if request.method == "POST":
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "landing.html",
                              {"message": "Invalid login"})
        return render(request, "landing.html")
    return render(request, "create.html")


def ran_gen(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def title_url(url):
    if url == "https://rickrolled.com":
        res1 = 'Rick Rolled'
        return res1
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    titles = []
    for title in soup.find_all('title'):
        titles.append(title.get_text())
    res = titles[0]
    return res


@csrf_exempt
def api(request, function):
    if function == "create":
        j = json.loads(request.body)
        if j['url']:
            if validators.url(j['url']):
                l = Link()
                l.owner = request.user
                c = ran_gen(
                    6,
                    "abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWSYZ1234567890-_~!*:@"
                )
                u = len(Link.objects.filter(slug=j["slug"]))
                a = u < 1
                if a == True:
                    if j["slug"]:
                        badLetters = False
                        if "?" in j["slug"] or "#" in j["slug"] or "&" in j[
                                "slug"] or "'" in j["slug"]:
                            badLetters = True
                        if bool(badLetters) == False:
                            l.slug = j["slug"]
                        elif bool(badLetters) == True:
                            res = {
                                "status": False,
                                "message": "Disallowed characters: ?&#'"
                            }
                            return HttpResponse(json.dumps(res))
                    else:
                        l.slug = c
                else:
                    l.slug = c
                l.url = j['url']
                l.title = title_url(j["url"])
                l.private = j['private']
                l.save()
                res = {
                    "status": True,
                    "message": "Succesfully created link!",
                    "data": {
                        "link": l.slug
                    }
                }
                if a == False:
                    res["message"] += " Just one thing: someone already took your custom slug so we generated one for you."
            else:
                res = {
                    "success":
                    False,
                    "message":
                    "That is not a valid url, what are you thinking mate"
                }
        else:
            res = {
                "sucess": False,
                "message":
                "There must be a url if you want to shorten a url."  # haha idiot lol
            }
        return HttpResponse(json.dumps(res))
    if function == "get":
        get_type = request.GET.get("type")
        if get_type == "links":
            time.sleep(1)
            return_res = list(reversed(
                Link.objects.filter(owner=request.user)))
            res = []
            for rese in return_res:
                m = model_to_dict(rese)
                res.append(m)
            return HttpResponse(json.dumps(res))
    if function == "title":
        try:
            url = Link.objects.filter(slug=request.GET.get("id"))[0].url
            if url == "https://rickrolled.com":
                res1 = '{"title": "Rick Rolled"}'
                return HttpResponse(res1)
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            titles = []
            for title in soup.find_all('title'):
                titles.append(title.get_text())
            res = titles[0]
            res1 = '{"title": "' + res + '"}'
            return HttpResponse(res1)
        except:
            return HttpResponse('{"title": "error"}')
    if function == "link":
        time.sleep(1)
        link = Link.objects.filter(slug=request.GET.get("id"))[0]
        return HttpResponse(json.dumps(model_to_dict(link)))
    if function == "delete":
        if request.method == "POST":
            link = Link.objects.filter(slug=request.GET.get("id"))[0]
            if link.owner == request.user:
                link.delete()
                return HttpResponse(
                    json.dumps({
                        "status": True,
                        "message": "Successfully deleted."
                    }))
            return HttpResponse(
                json.dumps({
                    "status": False,
                    "message": "Unauthorized"
                }))
    if function == "stat":
        res = []
        q = {
            '00': 0,
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0,
            '13': 0,
            '14': 0,
            '15': 0,
            '16': 0,
            '17': 0,
            '18': 0,
            '19': 0,
            '20': 0,
            '21': 0,
            '22': 0,
            '23': 0,
            '24': 0,
        }
        today = datetime.datetime.today()
        for e in Click.objects.all():
            if e.link.owner == request.user:  # if th e click is the user's
                if e.clicked.strftime('%Y-%m-%d') == today.strftime(
                        '%Y-%m-%d'):  # if the click is from today
                    q[e.clicked.strftime('%H')] += 1
        for key, value in q.items():
            res.append(value)
        return HttpResponse(str(res))
    return HttpResponse(
        "No such api function. Or maybe a post request and a get request. no one will know."
    )


def url_redirect(request, id):
    try:
        link = Link.objects.filter(slug=id)[0]
        c = Click()
        c.link = link
        c.save()
        link.clicks += 1
        link.save()
        return render(request, 'redirect.html', {"link": link})
    except:
        return render(request, "link-error.html")


def dashboard(request):
    if request.user.is_authenticated != True:
        if request.method == "POST":
            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("dashboard"))
            else:
                return render(request, "landing.html",
                              {"message": "Invalid username and/or password."})
        return render(request, "landing.html")
    else:
        return render(request, "dashboard.html")


def help(request):
    return render(request, "help.html")
