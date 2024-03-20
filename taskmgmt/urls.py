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
from groups import views as GroupViews

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('auth/', AuthViews.authenticate_view),
    path("", AuthViews.auth_view),
    path("auth/signin", AuthViews.signin, name="signin"),
    path('auth/signup', AuthViews.signup, name="signup"),
    path('auth/signout', AuthViews.signout, name="signup"),
    path('auth/', include("django.contrib.auth.urls"), name="auth"),

    path("task/list", TaskViews.task_list, name="task-list"),
    path("task/template", TaskViews.task_template_view),
    path("task/template/save", TaskViews.task_template_save),
    path("task/create", TaskViews.task_create, name="task_view"),
    path("task/<int:pk>", TaskViews.task_detail, name="task_detail"),
    path("task/<int:pk>/update", TaskViews.task_update, name="task_update"),
    path("task/<int:pk>/delete", TaskViews.task_delete, name="task_delete"),

    path("dashboard/", UserViews.user_dashboard_view, name="dashboard"),
    path("users/1/read", UserViews.save_user_info),
    path("users/1/edit", UserViews.update_user_info),

    path("groups/", GroupViews.group_list_view, name="group_list_view"),
    path("groups/create", GroupViews.create_group, name="group_create"),
    path("groups/<int:pk>/delete", GroupViews.delete_group, name="group_delete"),
    path("groups/<int:pk>", GroupViews.group_detail_view, name="group_detail_view"),
    path("groups/<int:pk>/task/create", GroupViews.create_group_task, name="create_group_task"),
    path("groups/<int:grp_pk>/task/<int:tsk_pk>", GroupViews.update_group_task),
    path("groups/<int:grp_pk>/users/<int:usr_pk>/delete", GroupViews.remove_user_from_group),

    path("groups/<int:pk>/invite/", GroupViews.invite_to_group),
    path("groups/invite/check_email", GroupViews.group_list_view),
]
