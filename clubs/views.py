from django.shortcuts import render


def clubs(request):
    return render(request, 'clubs/clubs.html')
