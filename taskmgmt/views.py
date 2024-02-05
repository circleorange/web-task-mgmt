from django.shortcuts import redirect, render
from django.http import HttpResponse

def test(request):
    return HttpResponse("test response")

def authentication_view(req):
    return render(
        request = req,
        template_name = "pages/authenticate.html",
        )

def authenticate(req):
    email = req.POST.get("email")
    print(f"authenticate().email.value: {email}")

    if email != "": return redirect("/dashboard")

    print(f"authenticate().email.invalid")
    
    context = { "email_err_msg": "Invalid Email" }

    return render(
        request = req,
        template_name = "pages/authenticate.html",
        context = context,
    )

def dashboard_view(req):
    return render(
        request = req,
        template_name = "pages/dashboard.html",
    )
