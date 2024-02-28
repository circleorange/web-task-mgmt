from django.shortcuts import redirect, render
from django.http import HttpResponse

def authenticate_view(req):
    return render(req, "authenticate.html")

# Authenticate User Credentials
def authenticate(req):
    email = req.POST.get("email")
    print(f"authenticate().email.value: {email}")

    if email == "": 
        print(f"authenticate().email.invalid")

        ctx = { "email_err_msg": "Invalid Email" }

        return render(req, "authenticate.html", ctx)

    # HX-Redirect header required to get HTMX update whole page
    response = HttpResponse(status=302)
    response['HX-Redirect'] = "/dashboard"
    return response
