import traceback
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Belongs
from tasks.forms import TaskForm
from tasks.models import Task

from users.models import CustomUser
from groups.models import Group
from .forms import GroupForm

def get_group_members(grp_pk):
    pass

def get_group_by_id(grp_pk):
    """
    Get group by primary key
    """
    try:
        group = get_object_or_404(Group, pk = grp_pk)
    except:
        print("get_group_by_id() - Failed to retrieve group")
        traceback.print_exc()
    return group


def is_valid_user_by_email(email):
    """
    Check whether user email address exists in the database
    """
    if email is None:
        return False

    if CustomUser.objects.filter(email = email).exists():
        return True

    return False


def get_user_by_email(usr_eml):
    """
    Return User object by email address
    """
    if is_valid_user_by_email(usr_eml):
        try:
            return CustomUser.objects.get(email = usr_eml)
        except:
            err_msg = 'Failed to retrieve user'
            print(f'get_user_by_email() - {err_msg}')
            traceback.print_exc()
            raise Exception(f'{err_msg}')
    else:
        invalid_usr_msg = 'User not found'
        raise Exception(f'{invalid_usr_msg}')


def is_user_already_member(req_usr, req_grp):
    """
    Returns True if user is already member of the group
    """
    if Belongs.objects.filter(user = req_usr, group = req_grp):
        return True
    
    return False


def group_invite(request, pk):
    req_eml = request.POST.get('email')
    print(f'group_invite() - provided email in request: {req_eml}')

    if not is_valid_user_by_email(req_eml):
        print('group_invite() - User email was not found in the database')
        return HttpResponse('User was not found with the provided email')
    
    usr = get_user_by_email(req_eml)
    grp = get_group_by_id(pk)

    try:
        Belongs.objects.create(user = usr, group = grp)
        return HttpResponse('User successfully added to the group')
    except:
        err_msg_grp_invite = 'Failed to add user to the group'
        print(f'group_invite() - {err_msg_grp_invite}')
        traceback.print_exc()
        return HttpResponse(f'{err_msg_grp_invite}, please try again later.')


def group_task_create(request, pk):
    print('group_task_create - Start')

    if request.method == 'GET':
        context = { 
            "task": TaskForm(),
            "status_choices": Task.Status.choices,
            "label_choices": Task.Label.choices,
            'create_group_task': True,
            'group_pk': pk,
            'form_action': f'/groups/{pk}/task/create'
        }
        return render(request, "task_view.html", { "context": context })
         
    if request.method == "POST":
        form = TaskForm(request.POST)

        print(f"task_create.POST.data: {request.POST}")

        if form.is_valid():
            try:
                task = form.save(commit = False)

                group = get_group_by_id(pk)
                task.group = group
                task.user = request.user

                task.save()
                print("task_create - Task has been successfully created")

                return redirect('group_get', pk = pk)

            except:
                print("task_create - Failed to create task")
                traceback.print_exc()
            
        else:
            print("task_create - Task has failed form validation")

    print("task_create - Unknown HTTP operation has been received")


def get_groups_by_user(usr):
    try:
        usr_grps = Belongs.objects.filter(user = usr)
        usr_grps_lst = [relation.group for relation in usr_grps]
        return usr_grps_lst
    except:
        err_msg_usr_grp = 'Failed to retrieve user groups'
        log_and_raise_exception(err_msg_usr_grp)


def log_and_raise_exception(msg):
    print(f'{msg}')
    traceback.print_exc()
    raise Exception(f'{msg}')


def get_user_by_id(usr_pk):
    try:
        return CustomUser.objects.get(id = usr_pk)
    except:
        err_msg = 'Failed to retrieve user by ID'
        log_and_raise_exception(err_msg)


def groups_view(request):
    usr = get_user_by_id(request.user.id)
    usr_grps = get_groups_by_user(usr)

    context = {
        "groups": usr_grps
    }

    return render(request, "groups_page.html", context)


def group_get(request, pk):
    """
    Function to retrieve view of specific group
    """
    # Provide Group details page
    try:
        group = get_object_or_404(Group, pk = pk)
        group_tasks = group.tasks.all()
        print(f'group_get - Group Tasks: {group_tasks}')

        context = {
            "group": group,
            'group_pk': pk,
            "tasks": group_tasks,
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


