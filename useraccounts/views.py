from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from useraccounts.forms import ChangeEmailForm
from clubs.models import ClubAdmin


@login_required
def account_settings(request):
    return render(request, "useraccounts/account_settings.html")


@login_required
def change_email(request):
    if request.method == "POST":
        form = ChangeEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your email has been updated.")
            return redirect("account_settings")
    else:
        form = ChangeEmailForm(instance=request.user)
    return render(request, "useraccounts/change_email.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        if request.POST.get("confirm_action"):
            user = request.user
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect("home")
        else:
            messages.warning(
                request, "You must confirm before deleting your account."
            )
    return render(request, "useraccounts/confirm_account_delete.html")


@login_required
def drop_club_admin_status(request):
    if request.method == "POST":
        if request.POST.get("confirm_action"):
            user = request.user
            club_admin = ClubAdmin.objects.filter(user=user).first()
            if club_admin:
                club_admin.delete()
                messages.success(
                    request, "Your account no longer has club admin status."
                )
            else:
                messages.warning(
                    request, "You do not currently have club admin status."
                )
            return redirect("account_settings")
        else:
            messages.warning(
                request,
                "You must confirm before dropping your club admin status.",
            )
    return render(request, "useraccounts/confirm_drop_club_admin_status.html")
