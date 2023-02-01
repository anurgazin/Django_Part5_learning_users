from django.shortcuts import render

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from basic_app.forms import UserProfileInfoForm, UserForm

# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile_info_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and user_profile_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = user_profile_info_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, user_profile_info_form.errors)
    else:
        user_form = UserForm()
        user_profile_info_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', context={'user_form': user_form,
                                                                   'profile_form': user_profile_info_form,
                                                                   'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('account is not active')
        else:
            print("login is failed")
            print('username: {}, password: {}'.format(username, password))
            return HttpResponse('invalid login')
    else:
        return render(request, 'basic_app/login.html', {})
