"""
URL configuration for taskmgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', views.authenticate_view, name='auth'),
    path('auth/validate', views.authenticate),
    path("dashboard/", views.dashboard_view),

    path("user/1", views.save_user_info),
    path("user/1/edit", views.update_user_info),
    path("dashboard/tasks", views.task_list_view),
    path("dashboard/templates", views.task_template_view),
]
