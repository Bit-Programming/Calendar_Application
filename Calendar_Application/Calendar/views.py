from django.http import HttpResponse
from django.template import loader

from .models import Question, Event
from django.utils import timezone

def index(request, date_begin, date_end):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # Validate date format
    try:
        date_begin = timezone.datetime.strptime(date_begin, "%Y-%m-%d")
        date_end = timezone.datetime.strptime(date_end, "%Y-%m-%d")
    except:
        return HttpResponse("Invalid date format. Please use the format YYYY-MM-DD")


    # Create array of arrays to store events for each day of the week
    event_list = []
    for i in range(7):
        event_list.append([])
    
    # Get the current day of the week adjusting values to make sunday 0 and saturday 6
    current_week_day = 0 if timezone.datetime.weekday(timezone.datetime.now()) + 1 == 7 else timezone.datetime.weekday(timezone.datetime.now()) + 1


    # Add events for before, the current day, and after
    for i in range(current_week_day + 1):
        event_list[i] = [f"{e.event_name} ({e.event_start_time}-{e.event_end_time})" for e in (Event.objects.filter(event_date=timezone.datetime.now() - timezone.timedelta(days=current_week_day - i)))]
    #event_list[current_week_day] = [f"{e.event_name} ({e.event_start_time}-{e.event_end_time})" for e in (Event.objects.filter(event_date=timezone.datetime.now()))]
    for i in range(6 - current_week_day):
        event_list[current_week_day + i + 1] = [f"{e.event_name} ({e.event_start_time}-{e.event_end_time})" for e in (Event.objects.filter(event_date=timezone.datetime.now() + timezone.timedelta(days=i + 1)))]


    


    template = loader.get_template("Calendar/index.html")
    context = {
        "latest_question_list": latest_question_list,
        "event_list": event_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):  
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)