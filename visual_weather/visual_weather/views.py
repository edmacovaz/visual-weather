from django.shortcuts import render_to_response
from datetime import date, datetime
from base import photos
from base import weather


def index(request):
    lat, lon = 52.529531, 13.411978
    when = request.GET.get("when", "today")
    matching_date = weather.date_matching_weather(lat, lon, when=when)
    urls = photos.search(matching_date)
    context = dict(urls=urls,
                   matching_date=matching_date)
    return render_to_response("master.html", context)


def for_day(request, day=''):
    day = datetime.strptime(day, "%Y-%m-%d")
    urls = photos.search(day)
    return render_to_response("master.html", dict(urls=urls))

