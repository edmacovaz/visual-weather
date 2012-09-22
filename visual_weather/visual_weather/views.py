from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from datetime import date, datetime
from base import photos
from base import weather


@cache_page(60*60)
def index(request):
    lat, lon = 52.529531, 13.411978
    when = request.GET.get("when", date.today().strftime("%Y/%m/%d"))
    matching_date = weather.date_matching_weather(lat, lon, when=when)
    year, month, day = matching_date.year, matching_date.month, matching_date.day
    urls = photos.search(year, month, day, lat=lat, lon=lon)
    context = dict(urls=urls,
                   matching_date=matching_date)
    return render_to_response("master.html", context)


@cache_page(60*60)
def for_day(request, day=''):
    year, month, day = day.split('-')
    urls = photos.search(int(year), int(month), int(day))
    return render_to_response("master.html", dict(urls=urls))

