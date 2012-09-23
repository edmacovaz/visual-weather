from urllib import urlencode
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from datetime import date, timedelta
from random import shuffle
from base import photos
from base import weather


def weekday_for_date(date):
    return date.strftime("%A")

def url_for_date(date):
    return "/?" + urlencode(dict(when=date.strftime("%Y/%m/%d")))


def index(request):
    lat, lon = 52.529531, 13.411978
    when = request.GET.get("when", date.today().strftime("%Y/%m/%d"))
    date_obj = date(*[int(x) for x in when.split("/")])

    weather_data = weather.get_data(lat, lon, when=when, number_days=1)

    current_data = dict(weekday=weekday_for_date(date_obj), data=weather_data[0])

    today = date.today()

    if date_obj == today:
        this_weather = "Today's weather looks"
    else:
        this_weather = "The weather for {date} will look".format(date=date_obj.strftime("%b. %d, %Y"))

    if date_obj > today:
        back_link = url_for_date(date_obj - timedelta(days=1))
    else:
        back_link = None

    forward_link = url_for_date(date_obj + timedelta(days=1))

    matching_date = weather.find_matches(current_data["data"], limit=1)[0].date
    year, month, day = matching_date.year, matching_date.month, matching_date.day
    urls = photos.search(year, month, day, lat=lat, lon=lon, limit=64, bust=2)
    shuffle(urls)

    context = dict(urls=urls,
                   matching_date=matching_date,
                   current_data=current_data,
                   this_weather=this_weather,
                   back_link=back_link,
                   forward_link=forward_link)

    return render_to_response("master.html", context)


def for_day(request, day='', lat='52.529531', lon='13.1411978'):
    year, month, day = day.split('-')
    urls = photos.search(int(year), int(month), int(day), lat, lon, bust=2)
    shuffle(urls)
    datum = date(int(year), int(month), int(day))
    context = dict(urls=urls,
                   year=year,
                   month=month,
                   day=datum.strftime("%d, %h %Y"),
                   )
    return render_to_response("remember.html", context)

