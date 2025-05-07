from django.shortcuts import render
from .models import ClubInfo


def clubs(request):
    test_club_info = ClubInfo.objects.first()
    return render(request, 'clubs/clubs.html', {"club_info": test_club_info})
