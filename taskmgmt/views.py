from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    return HttpResponse("test response")

def authentication_view(req):
    return render(
        request = req,
        template_name = "pages/authenticate.html",
        context = { "name": "Piotr" },
        )

def authenticate(req):
    print(f"validate().req: {req}")