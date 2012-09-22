import flickr

from datetime import timedelta

def search(day, location=('52.52992', '13.41157'), limit=10):
    """
    Return photos for the given date object.
    """
    end = day + timedelta(days=1)
    photos = flickr.photos_search(min_taken_date=day.strftime("%Y-%m-%d"),
                                  max_taken_date=end.strftime("%Y-%m-%d"),
                                  lat=location[0],
                                  lon=location[1],
                                  radius='5')[:limit]
    # TODO: just return URL of medium resolution image for now
    return [p.getMedium() for p in photos]

