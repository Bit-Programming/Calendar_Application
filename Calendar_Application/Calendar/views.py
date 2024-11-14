from datetime import timedelta


from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from .models import Event
from django.utils import timezone

def index(request, date, view):
    if view == "year":
        # Make sure date only contains a year
        try:
            date = timezone.datetime.strptime(date, "%Y")
        except:
            return HttpResponse("Invalid date format. Please use the format YYYY.")
        
        # Don't need to check for events if we're looking at a year

        # Temporary bc it looks cool
        event_list = requestEventDateRange(date, date + timedelta(days=365))
    elif view == "month":
        # Make sure date only contains a year and month day is optional
        try:
            date = timezone.datetime.strptime(date, "%Y-%m")
        except:
            try:
                date = timezone.datetime.strptime(date, "%Y-%m-%d")
            except:
                return HttpResponse("Invalid date format. Please use the format YYYY-MM or YYYY-MM-DD.")
        

        # Only need to check for 1 event per day if we're looking at a month
        first_day_of_month = date.replace(day=1)
        # Calculate the last day of the month
        if date.month == 12:
            last_day_of_month = date.replace(year=date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day_of_month = date.replace(month=date.month + 1, day=1) - timedelta(days=1)

        # Find the start of the week for the first day of the month (Sunday)
        start_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday() + 1)  # Adjust to Sunday
        
        # Fetch events for the entire month including surrounding days for the view
        event_list = requestEventDateRange(start_of_week, last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday())))

        # NOTE: HIDE EXTRA DAYS OF THE WEEK THAT ARE STILL SHOWN AT THE END OF THE MONTH ON A NEW LINE

    elif view == "week":
        try:
            # Parse date
            date = timezone.datetime.strptime(date, "%Y-%m-%d")

            # Find the Sunday before the date and make sunday displayed as the first day of the week
            date = date - timedelta(days=(date.weekday() + 1) % 7)

        except ValueError:
            return HttpResponse("Invalid date format. Please use YYYY-MM-DD for weeks.")

        # Show all events for the week
        event_list = requestEventDateRange(date, date + timedelta(days=6))
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


    template = loader.get_template("Calendar/index.html")
    context = {
        "event_list": event_list,
    }
    return HttpResponse(template.render(context, request))
    
def requestEventDateRange(date_begin, date_end):
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



def event_details_ajax(request, event_id):
    # Get the event object by ID
    event = Event.objects.filter(id=event_id).first()
    
    if event:
        # Return event data as JSON
        data = {
            'name': event.event_name,
            'description': event.event_description,
            'event_date': event.event_date.strftime("%B %d, %Y"),  # Format the date
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)


"""
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):  
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
"""
