from django.shortcuts import render

# Create your views here.
def task_list_view(req):
    print("dashboard().loadPage")

    return render(req, "templates/task_list.html")

def task_template_view(req):
    print("template().load")
    return render(req, "partials/task_template.html")

def task_list_view(req):
    print("task_list_view().load")
    return render(req, "partials/main.html")