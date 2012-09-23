import sys

import flickr

from datetime import date, datetime, timedelta

from base.cache import cache_result

@cache_result()
def search(year, month, day, lat=52.52992, lon=13.41157, limit=32, bust=1):
    """
    Return photos for the given date object.
    """
    start = date(year, month, day)
    end = start + timedelta(days=1)
    photos = flickr.photos_search(min_taken_date=start.strftime("%Y-%m-%d"),
                                  max_taken_date=end.strftime("%Y-%m-%d"),
                                  lat=str(lat),
                                  lon=str(lon),
                                  #sort='interestingness-desc',
                                  #geo_context='2',
                                  per_page=limit*2,
                                  radius='20')
    final = []
    users = set()
    removed = 0
    # Filter multiple photos by same user
    for photo in photos:
        if photo.owner.id not in users:
            final.append(photo)
            users.add(photo.owner.id)
        elif len(photos) - removed <= limit:
            # Don't remove if we'd end up with not enough photos
            final.append(photo)
        else:
            removed += 1

    return [(p.getMedium(), p.title) for p in final]


def facebook_search(year, month, day):
    raise NotImplementedError("Not ready yet")
    """
    url = 'https://api.facebook.com/method/fql.query?query='
    url = url + urlquote(query)
    response = urlopen(url)
    """
