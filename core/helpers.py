from __future__ import unicode_literals

import requests
import redis
import json
import os


def fetch_and_cache_data(
    api_arguments,
    hash
):
    token = os.environ["UCLAPI_TOKEN"]

    params = {
        "token": token,
        "results_per_page": "100"
    }

    for key in api_arguments:
        if api_arguments[key] != "":
            params[key] = api_arguments[key]

    req = requests.get(
        "https://uclapi.com/roombookings/bookings",
        params=params
    )
    resp = req.json()

    bookings = resp["bookings"]

    next_page = resp["next_page_exists"]
    counter = 0
    while next_page:
        page_token = resp["page_token"]
        params = {
            "token": token,
            "page_token": page_token
        }
        pagination_req = requests.get(
            "https://uclapi.com/roombookings/bookings",
            params=params
        )
        pagination_resp = pagination_req.json()
        bookings += pagination_resp["bookings"]
        if pagination_resp["next_page_exists"] and counter < 11:
            next_page = True
            counter += 1
        else:
            next_page = False

    redis_url = os.environ["REDIS_URL"]
    conn = redis.from_url(redis_url)

    querycache = conn.hgetall("querycache")

    querycache[hash] = json.dumps(bookings)

    conn.hmset("querycache", querycache)


def get_api_arguments_from_db(hash):
    from core.models import Query
    query = Query.objects.get(hash=hash)

    roomid = query.roomid
    start_datetime = query.start_datetime
    end_datetime = query.end_datetime
    date = query.date
    siteid = query.siteid
    description = query.description
    contact = query.contact
    api_arguments = {
        "roomid": roomid,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "date": date,
        "siteid": siteid,
        "description": description,
        "contact": contact
    }
    return api_arguments
