from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EnquiryForm


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if request.user.is_authenticated:
                enquiry.user = request.user
            enquiry.save()
            messages.success(
                request,
                "Your enquiry has been submitted successfully."
            )
            return redirect("contact")
        else:
            messages.warning(
                request,
                (
                    "Form data was invalid - please check the error message(s)"
                    " in the form and try again"
                )
            )
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data["email"] = request.user.email
        form = EnquiryForm(initial=initial_data)

    return render(request, "contact/contact.html", {"form": form})
