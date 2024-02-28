from django.http import HttpResponse
from django.shortcuts import redirect, render

tasks = []

def create_task_view(request):
    print("createTaskView")
    # GET request handles returning new task creation view
    if request.method == "GET":
        print("createTaskView.GET")
        return render(request, "create_task.html")

    # POST request handles when new task is created
    elif request.method == "POST":
        print("createTaskView.POST")

        # get task data and drop CSRF token
        task_data = {key: request.POST[key] for key in request.POST.keys()}
        task_data.pop("csrfmiddlewaretoken", None)

        print(task_data)

        # append task to session task list
        tasks.append(task_data)
        
        return redirect("task-list")
    else:
        print("createTaskView: Unhandled HTTP operation")

def task_list_view(request):
    print("taskListView")

    # retrieve tasks from session
    print(f"Session tasks: {tasks}")
    return render(request, "task_list.html", {"tasks": tasks})

def task_template_view(req):
    print("templateView.request")
    return render(req, "task_template.html")

def task_template_save(req):
    # Get template data
    template_data = {key: req.POST[key] for key in req.POST.keys()}

    # drop CSRD token from template data
    template_data.pop("csrfmiddlewaretoken", None)

    print(f"template data: {template_data}")

    return HttpResponse(status=200)