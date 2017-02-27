from celery import shared_task
from helpers import fetch_and_cache_data
from django.utils import timezone


@shared_task
def fetch_and_cache_task():
    from core.models import Query

    all_queries = Query.objects.all()
    print len(all_queries)
    for query in all_queries:
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
        query.last_started = timezone.now()
        query.save()
        commence_fetch_and_cache(api_arguments, query.uuid)


@shared_task
def commence_fetch_and_cache(api_arguments, uuid):
    fetch_and_cache_data(api_arguments, uuid)


@shared_task
def test():
    print "test"


@shared_task
def test2():
    test()
