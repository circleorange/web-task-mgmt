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
from django.urls import include, path
from authentication import views as AuthViews
from tasks import views as TaskViews
from users import views as UserViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('auth/', AuthViews.authenticate_view),
    path("", AuthViews.auth_view),
    path("signin/", AuthViews.signin, name="signin"),
    path('signup/', AuthViews.signup, name="signup"),
    path('auth/', include("django.contrib.auth.urls"), name="auth"),

    path("task/list", TaskViews.task_list_view, name="task-list"),
    path("task/template", TaskViews.task_template_view),
    path("task/template/save", TaskViews.task_template_save),
    path("task/create", TaskViews.create_task_view),

    path("dashboard/", UserViews.user_dashboard_view, name="dashboard"),
    path("users/1/read", UserViews.save_user_info),
    path("users/1/edit", UserViews.update_user_info),
]
