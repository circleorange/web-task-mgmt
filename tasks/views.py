from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from tasks.utils import *
from core.utils import log_and_raise_exception
from groups.utils import get_group_by_task, get_group_id_by_task
from .models import Task
from .forms import TaskForm
import traceback


def task_detail(request, pk):
    """
    Function designed for handling requests of existing tasks:
        - GET request: returns task detail view for task at specified Primary Key
    """
    if request.method == "GET":
        try:
            task = get_object_or_404(Task, pk = pk) 
            context = { 
                "task": task,
                "status_choices": Task.Status.choices,
                "label_choices": Task.Label.choices,
                'edit_mode': True,
                "update_task": True,
                'form_action': f'/task/{pk}/update'
            }
            if task.group is not None:
                context['update_task'] = False
                context['update_group_task'] = True
                context['grp_pk'] = get_group_id_by_task(task)
            
            return render(request, "task_view.html", { "context": context })
        except:
            print("task_detail - Failed to retrieve task")
            traceback.print_exc()

    return redirect("task-list")


def task_list(request):
    """
    Function designed to return the task list view, populated with user tasks
    """
    usr_tsk = get_tasks_by_user_id(request.user.id)
    return render(request, "task_list.html", { "tasks": usr_tsk })


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
            "update_task": False,
            'form_action': '/task/create'
        }
        return render(request, "task_view.html", { "context": context })
         
    if request.method == "POST":
        form = TaskForm(request.POST)

        print(f"task_create.POST.data: {request.POST}")

        if form.is_valid():
            try:
                task = form.save(commit = False)
                task.user = request.user
                task.save()
                print("task_create - Task has been successfully created")
            except:
                print("task_create - Failed to create task")
                traceback.print_exc()

            return redirect("task-list")
        else:
            print("task_create - Task has failed form validation")

    print("task_create - Unknown HTTP operation has been received")
    return render(request, "create_task.html", { "form": TaskForm() })
    

def task_update(request, pk):
    """
    Function designed for handling updates to task details view for task at specified Primary Key
    """
    try:
        task = get_object_or_404(Task, pk = pk)
        form = TaskForm(request.POST, instance = task)

        if form.is_valid():
            form.save()
            print(f"task_detail - Task has been successfully updated")
        else:
            print(f"task_detail - Task has failed form validation")

    except:
        print(f"task_detail - Failed to update task")
        traceback.print_exc()

    return redirect("task-list")


def task_delete(request, pk):
    """
    Function designed for handling delete requests for task of specified Primay Key
    """
    try:
        task = get_object_or_404(Task, pk = pk)
        task.delete()
        print("task_detail - Task has been successfully deleted")
    except:
        print(f"task_detail - Failed to delete task")
        traceback.print_exc()

    return redirect("task-list")


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
