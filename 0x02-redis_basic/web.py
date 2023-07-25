#!/usr/bin/env python3
'''A module with tools for request caching and tracking'''
import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """track howmany times a particular URL was accessed in the key
        "count:{url}"
        and cache the resultwith an experation time of 10 seconds"""

    r.set(f"cached:{url}", count)
    resp = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return resp.text


if _name == "_main_":
    get_page('http://slowly.robertomurray.co.uk')
