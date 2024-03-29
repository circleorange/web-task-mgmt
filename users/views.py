from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard_view(req):
    return render(req, "user_dashboard.html")

def update_user_info(req):
    return render(req, "user_info_edit.html")

def save_user_info(req):
    return render(req, "user_info_read.html")
