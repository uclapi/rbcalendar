from django_cal.views import Events
import os
import redis
import ciso8601
import json
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from core.models import Query
from django.utils import timezone
import helpers


def index(request):
    return render(request, 'core/index.html')


def new_query(request):
    try:
        roomid = request.GET["roomid"]
        start_datetime = request.GET["start_datetime"]
        end_datetime = request.GET["end_datetime"]
        date = request.GET["date"]
        siteid = request.GET["siteid"]
        description = request.GET["description"]
        contact = request.GET["contact"]
    except KeyError:
        return HttpResponseBadRequest(
            "invalid/insufficient query params supplied"
        )
    new_query = Query(
        roomid=roomid,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        date=date,
        siteid=siteid,
        description=description,
        contact=contact,
        last_started=timezone.now()
    )
    new_query.save()
    api_arguments = helpers.get_api_arguments_from_db(new_query.uuid)
    helpers.fetch_and_cache_data(api_arguments, new_query.uuid)

    return JsonResponse({
        "ok": True,
        "calendar_url": "http://{}/c/{}/events.ics".format(
            request.get_host(),
            new_query.uuid
        )
    })


class Bookings(Events):
    def get_object(self, *args, **kwargs):
        self.uuid = kwargs["uuid"]

    def items(self):

        redis_url = os.environ.get("REDIS_URL")
        conn = redis.from_url(redis_url)

        querycache = conn.hgetall("querycache")

        contact_data = json.loads(querycache[self.uuid])
        return contact_data

    def cal_name(self):
        return "Room bookings calendar"

    def cal_desc(self):
        return (
            "Generated thanks to UCL API"
        )

    def item_summary(self, item):
        return item["description"]

    def item_start(self, item):
        return ciso8601.parse_datetime(item["start_time"])

    def item_end(self, item):
        return ciso8601.parse_datetime(item["end_time"])

    def item_location(self, item):
        return item["roomname"]

    def item_uid(self, item):
        return "{}W{}".format(item["slotid"], item["weeknumber"])
