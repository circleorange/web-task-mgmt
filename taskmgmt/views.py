from django.shortcuts import redirect, render
from django.http import HttpResponse

user_info = {
        "fullName": "Test User",
        "email": "test@gmail.com",
        "company": "Some Company",
        "position": "Software Engineer",
    }

def authenticate_view(req):
    context = {
        "show_navbar": False,
    }

    return render(
        request = req,
        template_name = "pages/authenticate.html",
        context = context,
        )

# Authenticate User Credentials
def authenticate(req):
    email = req.POST.get("email")
    print(f"authenticate().email.value: {email}")

    if email == "": 
        print(f"authenticate().email.invalid")

        context = { "email_err_msg": "Invalid Email" }

        return render(
            request = req,
            template_name = "pages/authenticate.html",
            context = context,
        )

    # HX-Redirect header required to get HTMX update whole page
    response = HttpResponse(status=302)
    response['HX-Redirect'] = "/dashboard"
    return response

    
def dashboard_view(req):
    print("dashboard().loadPage")

    context = {
        "show_navbar": True,
    }
    context.update(user_info)

    return render(
        request = req,
        template_name = "pages/dashboard.html",
        context = context,
    )

def update_user_info(request):
    
    print(f"update_user_info().user_info.value: {user_info}")

    return render(
        request,
        "partials/user_info_edit.html",
        user_info,
    )

def save_user_info(request):

    return render(
        request,
        "partials/user_info_read.html",
        user_info,
    )