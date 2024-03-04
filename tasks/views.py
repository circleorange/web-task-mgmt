from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Task
from .forms import TaskForm

tasks = []

def task_detail(request, pk):
    """
    Function designed for handling GET requests to retrieve details of existing task. Arguments:
        - request
        - pk: Primary Key, the unique identifier for the record
    """
    context = { 
        "task": get_object_or_404(Task, pk = pk),
        "status_choices": Task.Status.choices,
        "label_choices": Task.Label.choices,
        "edit_mode": True,
    }

    return render(request, "task_view.html", { "context": context })


def task_list(request):
    """
    Function designed to return the task list view, populated with user tasks
    """
    tasks = Task.objects.all()

    print(f"task_list.tasks: {tasks}")

    return render(request, "task_list.html", { "tasks": tasks })


def task_create(request):
    """
    Function designed for handling GET and POST requests:
        - GET request: returns the task creation view
        - POST request: creates the task and redirects to task list view
    """
    if request.method == "GET":
        context = { 
            "task": TaskForm(),
            "status_choices": Task.Status.choices,
            "label_choices": Task.Label.choices,
            "edit_mode": False,
        }
        return render(request, "task_view.html", { "context": context })
         
    if request.method == "POST":
        form = TaskForm(request.POST)

        print(f"task_create.POST.data: {request.POST}")

        if form.is_valid():
            print("task_create.form.is_valid: true")

            task = form.save(commit = False)
            task.creator = request.user
            task.save()

            return redirect("task-list")
    else:
        form = TaskForm()
    
    return render(request, "create_task.html", { "form": form })


def task_update(request, pk):
    """
    Function designed for handling GET and POST requests:
        - GET request: returns task detail view for task at specified Primary Key
        - POST request: update task details of the task at specified Primary Key
    """
    task = get_object_or_404(Task, pk = pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance = task)

        if form.is_valid():
            form.save()
            return redirect("task-list")
    else:
        form = TaskForm(instance = task)

    return render(request, "task_form.html", { "form": form })


def task_delete(request, pk):
    """
    Function designed for handling POSTS requests:
        - POST request: delete task of specified Primay Key
    """
    task = get_object_or_404(Task, pk = pk)

    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    
    return render(request, "task_form.html", { "object": task })


def create_task_view(request):
    print("createTaskView")
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
