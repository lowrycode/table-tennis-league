from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def account_settings(request):
    return render(request, 'useraccounts/account_settings.html')
