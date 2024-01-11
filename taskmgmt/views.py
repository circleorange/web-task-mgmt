from django.shortcuts import render

def authentication_view(request):
    return render(request, "pages/authenticate.html")