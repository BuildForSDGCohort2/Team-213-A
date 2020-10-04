from django.forms import ModelForm
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['start_date', 'end_date', 'all_day', 'repeat', 'end_repeat', 'title', 'description', 'categories']
