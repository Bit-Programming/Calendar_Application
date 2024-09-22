from django.db import models

from django.db import models
from django.utils import timezone


class Event(models.Model):
    event_date = models.DateField("Event Date")
    event_start_time = models.TimeField("Event Start Time")
    event_end_time = models.TimeField("Event End Time")
    event_name = models.CharField(max_length=200)
    event_description = models.TextField()
    def __str__(self):
        return self.event_name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text