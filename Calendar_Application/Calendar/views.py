from django.http import HttpResponse
from django.template import loader

from .models import Question, Event
from django.utils import timezone

def index(request, date, view):
    if view == "year":
        # Make sure date only contains a year
        try:
            date = timezone.datetime.strptime(date, "%Y")
        except:
            return HttpResponse("Invalid date format. Please use the format YYYY.")
        
        # Don't need to check for events if we're looking at a year
    elif view == "month":
        # Make sure date only contains a year and month
        try:
            date = timezone.datetime.strptime(date, "%Y-%m")
        except:
            return HttpResponse("Invalid date format. Please use the format YYYY-MM.")

        # Only need to check for 1 event per day if we're looking at a month
    elif view == "week":
        # Make sure date only contains a year, month, and day of beginning of the week
        try:
            # Make sure date is formatted properly
            date = timezone.datetime.strptime(date, "%Y-%m-%d")

            # Make sure date is the beginning of the week
            if date.weekday() != 6:
                return HttpResponse("Invalid date. Please use the beginning of the week (Sunday) in the format YYYY-MM-DD.")
        except:
            return HttpResponse("Invalid date format. Please use the format YYYY-MM-DD.")

        # Show all events for the week
        event_list = requestEventDateRange(date, date + timezone.timedelta(days=6))
    elif view == "day":
        # Make sure date only contains a year, month, and day
        try:
            date = timezone.datetime.strptime(date, "%Y-%m-%d")
        except:
            return HttpResponse("Invalid date format. Please use the format YYYY-MM-DD.")
        
        # Show all events for the day
        event_list = requestEventDateRange(date, date)
        
    else:
        return HttpResponse("Invalid view. Please use 'day', 'week', 'year', or 'month'.")

    latest_question_list = Question.objects.order_by("-pub_date")[:5]



    # Temporary
    first=list(event_list.keys())[0]
    template = loader.get_template("Calendar/index.html")
    context = {
        "latest_question_list": latest_question_list,
        "event_list": event_list,
        "first": first,
    }
    return HttpResponse(template.render(context, request))


def requestEventDateRange(date_begin, date_end):
    # Create object to store events
    event_list = {
    #   "2024-01-01": [event1, event2, etc.],
    #   "2024-01-02": [event1, event2, etc.],
    }

    # Get all events between the two dates
    # NOTE: Requesting many events could slow down the server
    for i in range((date_end - date_begin).days + 1):
        event_date = date_begin + timezone.timedelta(days=i)
        events = list(Event.objects.filter(event_date=event_date))
        #if events:
        print("EVENTS:", events)
        event_list[event_date.strftime("%Y-%m-%d")] = events
    return event_list


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):  
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)