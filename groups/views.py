import traceback
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Belongs
from tasks.forms import TaskForm
from tasks.models import Task

from users.models import CustomUser
from groups.models import Group
from .forms import GroupForm

def group_task_list(request):
    pass

def group_task_create(request, pk):
    print('group_task_create - Start')

    if request.method == 'GET':
        context = { 
            "task": TaskForm(),
            "status_choices": Task.Status.choices,
            "label_choices": Task.Label.choices,
            "edit_mode": False,
            'group_task': True,
            'group_pk': pk,
        }
        return render(request, "task_view.html", { "context": context })
         
    if request.method == "POST":
        form = TaskForm(request.POST)

        print(f"task_create.POST.data: {request.POST}")

        if form.is_valid():
            try:
                task = form.save(commit = False)
                task.creator = request.user
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


def groups_view(request):
    context = {}
    try:
        # group_list = request.user.user_groups.all()
        user_loggedIn = CustomUser.objects.get(id = request.user.id)

        # query Belongs model for user groups
        user_belongs = Belongs.objects.filter(user = user_loggedIn)

        # extract user groups
        user_groups = [relation.group for relation in user_belongs]

        print(f"groups_view - User Groups: {user_groups}")

        context = {
            "groups": user_groups
        }
        print("groups_view - User groups have been successfully retrieved")

    except:
        print("groups_view - Failed to retrieve user groups")
        traceback.print_exc()

    return render(request, "groups_page.html", context)


def group_get(request, pk):
    """
    Function to retrieve view of specific group
    """
    # Provide Group details page
    if request.method == "GET":
        try:
            context = {
                "group": get_object_or_404(Group, pk = pk)
            }
            return render(request, "group.html", context)
        except:
            print("group_get - Failed to retrieve group")
            traceback.print_exc()


def group_create(request):
    # Provide Group creation page
    if request.method == "GET":
        try:
            # retrieve the group form and respond to client
            context = {
                "form": GroupForm(),
            }
            return render(request, "group_create.html", context)
        except:
            traceback.print_exc()
    
    # Handle group creation
    if request.method == "POST":
        group_form = GroupForm(request.POST)

        if group_form.is_valid():

            group = group_form.save()

            Belongs.objects.create(
                user = request.user,
                group = group
            )

            print("group_create - Group was successfully created")

            return redirect("groups_view")
        
        else:
            print("group_create - Failed to create group")
            traceback.print_exc()
             

def group_delete(request, pk):
    """
    Function designed to handle delete requests for group at specified kek
    """
    try:
        group = get_object_or_404(Group, pk = pk)
        group.delete()
        print("group_delete - Successfully deleted group")
    except:
        print("group_delete - Failed to delete group")
        traceback.print_exc()

    return redirect("groups_view")

def group_invite():
    pass

