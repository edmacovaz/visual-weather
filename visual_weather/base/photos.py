import sys

import flickr

from datetime import datetime, timedelta

def search(day, lat='52.52992', lon='13.41157', limit=32):
    """
    Return photos for the given date object.
    """
    end = day + timedelta(days=1)
    photos = flickr.photos_search(min_taken_date=day.strftime("%Y-%m-%d"),
                                  max_taken_date=end.strftime("%Y-%m-%d"),
                                  lat=lat,
                                  lon=lon,
                                  #geo_context='2',
                                  per_page=limit,
                                  radius='5')
    # TODO: just return URL of medium resolution image for now
    return [p.getMedium() for p in photos]
