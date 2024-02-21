from django.shortcuts import render

def update_user_info(req):
    return render(req, "templates/user_info_edit.html")

def save_user_info(req):
    return render(req, "templates/user_info_read.html")