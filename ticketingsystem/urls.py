"""
URL configuration for Ticketingsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ticketapp import views
from django.urls import path, include
from ticketapp.views import ticket_volume_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ticket_list/',views.ticket_list,name='ticket_list'),
    path('ticket_create/',views.ticket_create,name='ticket_create'),
    path('ticket/<int:ticket_id>/update_status/', views.update_ticket_status, name='update_ticket_status'),
    path('ticket_filter/', views.ticket_filter, name='ticket_filter'),
    path('dashboard/ticket-volume/', ticket_volume_dashboard, name='ticket_volume_dashboard'),
    path('client_status/', views.client_status, name='client_status'),
    path('client_onboarding/', views.client_onboarding_list, name='client_onboarding_list'),
    path('client_onboarding/add/', views.client_onboarding_add, name='client_onboarding_add'),
    path('client-onboarding/<int:pk>/update-status/', views.update_client_status, name='update_client_status'),
    path('dashboard/', views.onboarding_dashboard, name='onboarding_dashboard'),

]
