# core/views.py
from django.shortcuts import render


def group_view(request):
    return render(request, 'core/gc.html')
