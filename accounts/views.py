from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import UserCreationForm


class HomeView(generic.TemplateView):
    template_name = "home.html"


class DashboardView(LoginRequiredMixin, generic.TemplateView):
    permissions = ["is_authenticated"]

    def get_template_names(self):
        if self.request.user.user_type == 1:
            return "dashboard_doctor.html"

        return "dashboard_patient.html"


def AccountCreateView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except Exception as e:
                form.add_error(None, e)

            login(request, user)
            return redirect(reverse("dashboard"))

    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})
