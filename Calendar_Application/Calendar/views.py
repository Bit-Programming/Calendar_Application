from datetime import timedelta


from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader

from .models import Event
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import get_list_or_404

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


@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        try:
            event_name = request.POST['event_name']
            event_date = request.POST['event_date']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            description = request.POST.get('description', '')
            place = request.POST.get('place', '')
            color = request.POST.get('event_color', '#496DDB')

            # Create the event
            new_event = Event.objects.create(
                event_date=event_date,
                event_start_time=start_time,
                event_end_time=end_time,
                event_name=event_name,
                event_description=description,
                event_place=place,
                event_color=color
            )
            new_event.save()
            return JsonResponse({'success': True, 'message': 'Event created successfully.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            Event.objects.filter(id=event_id).delete()
            
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})

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

def events_for_date(request, date):
    events = get_list_or_404(Event, event_date=date)
    event_data = [{
        'name': event.event_name,
        'description': event.event_description,
        'start_time': event.event_start_time,
        'end_time': event.event_end_time,
        'place': event.event_place,
        'color': event.event_color,
        'id': event.pk
    } for event in events]
    return JsonResponse({'events': event_data})

def index(request, date, view):

    # Main template
    template = loader.get_template("Calendar/index.html")


    date_obj = parse_date(date, view)

    first_day_of_view = date_obj.strftime("%Y-%m-%d")

    week_heading = ""

    if not date_obj:
        return HttpResponse("Invalid date format. Please use the correct format.")

    if view == VIEW_YEAR:
        # Sketch but works for now
        first_day_of_view = (date_obj + timedelta(days=7)).strftime("%Y-01-01")
        # Don't need to check for events if we're looking at a year but doing it temporarily bc it looks cool

        # Account for leapyears when calculating the end date
        date_start = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7)
        date_end = date_obj + (timedelta(days=366) if (date_obj.year % 4 == 0 and (date_obj.year % 100 != 0 or date_obj.year % 400 == 0)) else timedelta(days=365))

        event_list = request_event_date_range(date_start, date_end)
    elif view == VIEW_MONTH:
        # Sketch but works for now
        first_day_of_view = (date_obj + timedelta(days=7)).strftime("%Y-%m-01")

        first_day_of_month = date_obj.replace(day=1)


        #date_end = date_obj.replace(day=1) + timedelta(days=31)
        #date_end = date_end.replace(day=1) - timedelta(days=1)
        #date_end = date_end + timedelta(days=5 - date_end.weekday())

        # date_end is the rest of the days in the week of the last day of the month

        date_start = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7)

        # Calculate the last day of the month
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        
        # Extend date_end to the Saturday after the last day of the month
        days_to_saturday = (5 - last_day_of_month.weekday()) % 7
        date_end = last_day_of_month + timedelta(days=days_to_saturday)

        # TODO: Only need to check for 1 event per day if we're looking at a month

        # Fetch events for the extended range
        event_list = request_event_date_range(date_start, date_end)
    elif view == VIEW_WEEK:
        date_start = date_obj - timedelta(days=(date_obj.weekday() + 1) % 7) # Results in overflow error when year is 1 on January 1st
        event_list = request_event_date_range(date_start, date_start + timedelta(days=6))
        week_heading = date_start.strftime("%B %d, %Y") + " to " + (date_start + timedelta(days=6)).strftime("%B %d, %Y")
    elif view == VIEW_DAY:
        # Change the main template for day views
        template = loader.get_template("Calendar/day.html")


        event_list = request_event_date_range(date_obj, date_obj)
    else:
        return HttpResponse("Invalid view. Please use 'day', 'week', 'year', or 'month'.")


    title_text = {
        VIEW_YEAR: date_obj.strftime("%Y"),
        VIEW_MONTH: date_obj.strftime("%B %Y"),
        VIEW_WEEK: "Week of " + week_heading,
        VIEW_DAY: date_obj.strftime("%B %d, %Y")
    }.get(view)

    print("date_start:", first_day_of_view)

    context = {
        "event_list": event_list,
        "title_text": title_text,
        "date": date,
        "view": view,
        "first_day_of_view": first_day_of_view,
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
            'start_time': event.event_start_time,
            'end_time': event.event_end_time,
            'place': event.event_place,
            'color': event.event_color
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)
