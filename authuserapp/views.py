from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse
from .forms import LoginUserForm


# homepage
def index(request):
    # redirect user if already logged in
    if request.user.is_authenticated:
        # return HttpResponseRedirect(reverse("dashboard:dashboardhome"))
        return HttpResponseRedirect(reverse("dashboard:index-orders"))

    if request.method == 'POST':
        form = LoginUserForm(request.POST)

        if form.is_valid():
            userId = form.cleaned_data["user_id"]

            # check if user exists
            user = authenticate(request, username=userId, password=userId)
            if not user:
                user = User.objects.create_user(userId, None, userId)
                user.save()

            login(request, user)
            # return HttpResponseRedirect(reverse("dashboard:dashboardhome"))
            return HttpResponseRedirect(reverse("dashboard:index-orders"))

    else:
        form = LoginUserForm()

    return render(request, 'authuserapp/index.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('authuserapp:authhome')


# logged in user dashboard
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'authuserapp/dashboard.html')

    else:
        return redirect('authuserapp:authhome')
