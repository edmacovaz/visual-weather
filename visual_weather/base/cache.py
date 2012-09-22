from functools import wraps
import hashlib
from django.core.cache import cache


def _get_cache_key(func, args, kwargs):
    caching_keys = [func.__name__]

    if args is not None:
        caching_keys.extend(args)

    if kwargs is not None:
        caching_keys.extend(sorted(kwargs.iteritems()))

    caching_keys = [unicode(key) for key in caching_keys]
    cache_key = u'_'.join(caching_keys)
    return hashlib.sha512(cache_key).hexdigest()


def cache_result(timeout=60*60*24, do_not_cache=()):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = _get_cache_key(func, args, kwargs)

            # Fetch from cache
            output = cache.get(cache_key)
            if output is None:
                output = func(*args, **kwargs)
                if output not in do_not_cache:
                    cache.set(cache_key, output, timeout)
            return output

        return wrapper

    return decorator


def invalidate_result(func, *args, **kwargs):

    cache_key = _get_cache_key(func, args, kwargs)
    cache.delete(cache_key)

