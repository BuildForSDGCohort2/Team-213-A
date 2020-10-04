from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.shortcuts import render
import json


def index(request):
    return render(request, 'chat/index.html')


@login_required(login_url='/login/')
def room(request, room_name):
    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'chat/room.html', context)
