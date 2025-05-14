from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from useraccounts.forms import ChangeEmailForm


@login_required
def account_settings(request):
    return render(request, 'useraccounts/account_settings.html')


@login_required
def change_email(request):
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your email has been updated."
            )
            return redirect('account_settings')
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, 'useraccounts/change_email.html', {"form": form})
