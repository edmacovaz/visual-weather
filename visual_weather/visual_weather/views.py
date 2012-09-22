from urllib import urlencode
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from datetime import date, timedelta
from base import photos
from base import weather


def weekday_for_date(date):
    return date.strftime("%A")

def url_for_date(date):
    return urlencode(dict(when=date.strftime("%Y/%m/%d")))


def index(request):
    lat, lon = 52.529531, 13.411978
    when = request.GET.get("when", date.today().strftime("%Y/%m/%d"))
    date_obj = date(*[int(x) for x in when.split("/")])

    weather_data = weather.get_data(lat, lon, when=when, number_days=3)

    current_data = dict(weekday=weekday_for_date(date_obj), data=weather_data[0])

    tomorrow = date_obj + timedelta(days=1)
    tomorrows_data = dict(weekday=weekday_for_date(tomorrow),
                          url=url_for_date(tomorrow),
                          data=weather_data[1])
    after_tomorrow = date_obj + timedelta(days=2)
    after_tomorrows_data = dict(weekday=weekday_for_date(after_tomorrow),
                                url=url_for_date(after_tomorrow),
                                data=weather_data[2])

    matching_date = weather.find_matches(current_data["data"], limit=1)[0].date
    year, month, day = matching_date.year, matching_date.month, matching_date.day
    urls = photos.search(year, month, day, lat=lat, lon=lon)

    context = dict(urls=urls,
                   matching_date=matching_date,
                   current_data=current_data,
                   tomorrows_data=tomorrows_data,
                   after_tomorrows_data=after_tomorrows_data,)

    return render_to_response("master.html", context)


@cache_page(60*60)
def for_day(request, day=''):
    year, month, day = day.split('-')
    urls = photos.search(int(year), int(month), int(day))
    return render_to_response("master.html", dict(urls=urls))

