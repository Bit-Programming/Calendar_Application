from datetime import timedelta


from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from .models import Event
from django.utils import timezone


# CONSTANTS

# Constants for views
VIEW_YEAR = "year"
VIEW_MONTH = "month"
VIEW_WEEK = "week"
VIEW_DAY = "day"

DATE_FORMATS = {
    VIEW_YEAR: "%Y",
    VIEW_MONTH: "%Y-%m",
    VIEW_WEEK: "%Y-%m-%d",
    VIEW_DAY: "%Y-%m-%d",
}

def parse_date(date_str, view):
    # Parse date string based on view and return a date object or None.
    try:
        return timezone.datetime.strptime(date_str, DATE_FORMATS[view])
    except (ValueError, KeyError):
        return None

def request_event_date_range(date_begin, date_end):
    # Fetch all events between date_begin and date_end
    event_list = []
    for i in range((date_end - date_begin).days + 1):
        event_date = date_begin + timezone.timedelta(days=i)
        events = list(Event.objects.filter(event_date=event_date))
        event_list.append({
            'date': event_date.strftime("%Y-%m-%d"),
            'weekday': event_date.strftime("%A"),
            'events': events
        })
    return event_list


def index(request, date, view):
    date_obj = parse_date(date, view)
    if not date_obj:
        return HttpResponse("Invalid date format. Please use the correct format.")

    if view == VIEW_YEAR:
        # Don't need to check for events if we're looking at a year but doing it temporarily bc it looks cool

        # Account for leapyears when calculating the end date
        date_start = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7)
        date_end = date_obj + (timedelta(days=366) if (date_obj.year % 4 == 0 and (date_obj.year % 100 != 0 or date_obj.year % 400 == 0)) else timedelta(days=365))

        event_list = request_event_date_range(date_start, date_end)
    elif view == VIEW_MONTH:
        date_end = date_obj.replace(day=1) + timedelta(days=31)
        date_end = date_end.replace(day=1) - timedelta(days=1)
        first_day_of_week = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7)
        last_day_of_week = date_end + timedelta(days=6 - date_end.weekday())
        event_list = request_event_date_range(first_day_of_week, last_day_of_week)
        # TODO: Only need to check for 1 event per day if we're looking at a month
    elif view == "week":
        start_of_week = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7) # Results in overflow error when year is 1 on January 1st
        event_list = request_event_date_range(start_of_week, start_of_week + timedelta(days=6))
    elif view == "day":
        event_list = request_event_date_range(date_obj, date_obj)
    else:
        return HttpResponse("Invalid view. Please use 'day', 'week', 'year', or 'month'.")


    title_text = {
        VIEW_YEAR: date_obj.strftime("%Y"),
        VIEW_MONTH: date_obj.strftime("%B %Y"),
        VIEW_WEEK: "Week of " + date_obj.strftime("%B %d, %Y"),
        VIEW_DAY: date_obj.strftime("%B %d, %Y")
    }.get(view)

    template = loader.get_template("Calendar/index.html")
    context = {
        "event_list": event_list,
        "title_text": title_text,
        "view": view,
    }
    return HttpResponse(template.render(context, request))



def event_details_ajax(request, event_id):
    # Get the event object by ID
    event = Event.objects.filter(id=event_id).first()
    
    if event:
        # Return event data as JSON
        data = {
            'name': event.event_name,
            'description': event.event_description,
            'event_date': event.event_date.strftime("%B %d, %Y"),
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)
