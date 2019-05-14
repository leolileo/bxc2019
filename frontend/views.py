import os

from django.shortcuts import render


def index(request):
    data_from_server = {"data_from_server": "my name is leo", "good": "good", "problem": "problem", "alert": "alert",
                        "status": os.environ['APP_VAR_WHATEVER']}
    os.environ['APP_VAR_WHATEVER'] = "good"
    return render(request, 'index.html', context=data_from_server)


def problem(request):
    print("CHANGED")
    os.environ['APP_VAR_WHATEVER'] = "problem"


def alert(request):
    print("CHANGED")
    os.environ['APP_VAR_WHATEVER'] = "alert"
