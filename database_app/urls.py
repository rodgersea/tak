from django.contrib.auth import views as auth_views
from database_app import views as user_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # user registraion and login
    path('register/',
         views.register,
         name='register'),
    path('login/',
         views.loginuser,
         name='login'),
    path('logout/',
         views.LogOut.as_view(),
         name='logout'),

    # landing page
    path('',
         user_views.home,
         name='home'),

    path('route/add',
         views.route_create,
         name='route-add'),
    path('add_route/',
         views.route_create,
         name='route-form'),

    path('save_route/',
         views.save_route,
         name='save-route'),
    path('saved_climb/',
         views.saved_climb,
         name='saved-climb'),

    path('session/',
         views.add_session,
         name='session'),
    path('session_form/<int:route_id>/',
         views.session_form,
         name='session-form'),
    path('session_form/<int:route_id>/create_session/',
         views.create_session,
         name='add-session'),

    path('open_projects/',
         views.OpenProjects.as_view(),
         name='open-projects'),
    path('project_details/<int:route_id>/',
         views.project_view,
         name='project-details'),
]
