from django.shortcuts import render_to_response
from datetime import date, datetime
from base import photos


def index(request):
    urls = photos.search(date(2012, 6, 1))
    return render_to_response("master.html", dict(urls=urls))


def for_day(request, day=''):
    day = datetime.strptime(day, "%Y-%m-%d")
    urls = photos.search(day)
    return render_to_response("master.html", dict(urls=urls))

