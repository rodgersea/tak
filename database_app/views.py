from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.views import generic
from datetime import date
from .models import *
from .forms import *
try:
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    user_model = User


# landing page
def home(request):
    return render(request,
                  'home.html')


# register new user - redirect to login page
class SignUp(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'user created, now login'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             'invalid')
        return redirect('login')


# login user - redirect to home page
# change extended base html once user authenticated
class LogIn(generic.View):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = LoginUserForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(
                        request, f'You are logged in as {username}')
                    return redirect('home')
                else:
                    messages.error(request, 'Error')
            else:
                messages.error(request, 'Username or password incorrect')
        form = LoginUserForm()
        return render(request, 'databasenew/login.html', {'form': form})


# logout user - redirect to unauthenticated homepage
class LogOut(LoginRequiredMixin, generic.View):
    login_url = 'login'

    def get(self, request):
        logout(request)
        messages.success(request, 'User logged out')
        return redirect('home')


# loads html page with context data to add a route to the general database
def route_create(request):
    form = ClimbElementForm()
    context = {
        'route_model': Route.objects.all(),
        'areas': Route.objects.all().values_list('area', flat=True).distinct(),
        'sectors': Route.objects.all().values_list('sector', flat=True).distinct(),
        'crags': Route.objects.all().values_list('crag', flat=True).distinct(),
        'walls': Route.objects.all().values_list('wall', flat=True).distinct(),
        'routes': Route.objects.all().values_list('route', flat=True).distinct(),
        'last_added': Route.objects.last(),
        'form': form,
    }
    if request.method == 'POST':
        route = request.POST['route_name']
        wall = request.POST['wall_name']
        crag = request.POST['crag_name']
        sector = request.POST['sector_name']
        area = request.POST['area_name']

        if route and not Route.objects.filter(route=route,
                                              wall=wall,
                                              crag=crag,
                                              sector=sector,
                                              area=area):
            new_route = Route(route=route,
                              wall=wall,
                              crag=crag,
                              sector=sector,
                              area=area)
            new_route.save()
            return HttpResponseRedirect(reverse('route-form'))
        else:
            return HttpResponseRedirect(reverse('route-add'))

    return render(request,
                  'database_app/route_form.html',
                  context=context)


# method to add route, could this be added with an if mehtod == POST to route_create()?
def add_route(request):
    if request.method == 'POST':
        route = request.POST['route_name']
        wall = request.POST['wall_name']
        crag = request.POST['crag_name']
        sector = request.POST['sector_name']
        area = request.POST['area_name']

        if route and not Route.objects.filter(route=route,
                                              wall=wall,
                                              crag=crag,
                                              sector=sector,
                                              area=area):
            new_route = Route(route=route,
                              wall=wall,
                              crag=crag,
                              sector=sector,
                              area=area)
            new_route.save()
            return HttpResponseRedirect(reverse('route-form'))
        else:
            return HttpResponseRedirect(reverse('route-add'))


# loads html page with context data to add route to user's list of open projects
def save_route(request):
    context = {
        'routes': Route.objects.all(),
        'saved_routes': SavedClimb.objects.all()
    }
    return render(request,
                  'database_app/save_route.html',
                  context=context)


# function to save route to user's database of open projects
# could this be added to save_route()?
def saved_climb(request):
    route = Route.objects.get(route=request.POST['route_name'])

    if not SavedClimb.objects.filter(route=route):
        newclimb = SavedClimb(user=request.user,
                              route=route)
        newclimb.save()
        return redirect('save-route')
    else:
        return redirect('save-route')


# loads html with context to add session to specific route in user's list of open projects
def add_session(request):
    context = {
        'routes': SavedClimb.objects.all()
    }
    return render(request,
                  'database_app/add_session.html',
                  context=context)


# loads html page with context data to add a session to the current project
def session_form(request, route_id):
    context = {
        'route': Route.objects.get(id=route_id),
        'route_model': Route.objects.all(),
        'form': ClimbElementForm(),
        'areas': Route.objects.all().values_list('area', flat=True).distinct(),
        'sectors': Route.objects.all().values_list('sector', flat=True).distinct(),
        'crags': Route.objects.all().values_list('crag', flat=True).distinct(),
        'walls': Route.objects.all().values_list('wall', flat=True).distinct(),
        'routes': Route.objects.all().values_list('route', flat=True).distinct(),
    }
    return render(request,
                  'database_app/session_form.html',
                  context=context)


# create session object linked to user and route
def create_session(request, route_id):
    route = Route.objects.get(id=route_id)
    pass_session = request.POST['session_name']
    pass_attempt = request.POST['attempt_name']
    pass_date = request.POST['date_name']
    pass_notes = request.POST['notes_name']

    if not Attempt.objects.filter(route=route,
                                  session=pass_session,
                                  attempt=pass_attempt):
        attempt = Attempt(user=request.user,
                          route=route,
                          session=pass_session,
                          attempt=pass_attempt,
                          date=pass_date,
                          notes=pass_notes)
        attempt.save()
        return redirect('session')


# displays list of user's open projects
class OpenProjects(ListView):
    model = SavedClimb
    template_name = 'database_app/open_projects.html'

    def get_queryset(self):
        return SavedClimb.objects.filter(user=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        context['savedclimbs'] = SavedClimb.objects.filter(user=self.request.user)
        return context


# detail type view for a user's specific project
# html displays project info in cards
def project_view(request, route_id):
    attempts = Attempt.objects.filter(route=route_id)
    sessions = Attempt.objects.filter(route=route_id).values_list('session', flat=True).distinct()

    context = {
        'route': Route.objects.get(id=route_id),
        'attempts': attempts,
        'sessions': sessions,
    }
    return render(request,
                  'database_app/project_details.html',
                  context=context)
