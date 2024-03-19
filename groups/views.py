import traceback
from django.http import HttpResponse
from django.shortcuts import redirect, render
from core.models import Belongs
from groups.utils import *
from users.utils import *
from tasks.forms import TaskForm
from tasks.models import Task

from .forms import GroupForm


def invite_to_group(request, pk):
    req_eml = request.POST.get('email')
    print(f'invite_to_group() - provided email in request: {req_eml}')

    if not is_valid_user_by_email(req_eml):
        print('invite_to_group() - User email was not found in the database')
        return HttpResponse('User was not found with the provided email')
    
    usr = get_user_by_email(req_eml)
    grp = get_group_by_id(pk)

    try:
        Belongs.objects.create(user = usr, group = grp)
        return HttpResponse('User successfully added to the group')
    except:
        err_msg = 'Failed to add user to the group'
        log_and_raise_exception(err_msg)
        return HttpResponse(f'{err_msg}, please try again later.')


def create_group_task(request, pk):
    print('create_group_task - Start')

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

        if form.is_valid():
            task = form.save(commit = False)
            grp = get_group_by_id(pk)
            task.group = grp
            task.user = request.user
            task.save()

            print("task_create - Task has been successfully created")
            return redirect('group_detail_view', pk = pk)
        else:
            print("task_create - Task has failed form validation")


def group_list_view(request):
    usr = get_user_by_id(request.user.id)
    usr_grp = get_groups_by_user(usr)

    context = {
        "groups": usr_grp
    }
    return render(request, "groups_page.html", context)


def group_detail_view(request, pk):
    """
    View returning Group Details page
    """
    # Provide Group details page
    grp = get_group_by_id(pk)
    grp_tsk = get_tasks_by_group(grp)
    grp_usr = get_users_by_group(grp)

    grp_tsk_len = len(grp_tsk)
    grp_usr_len = len(grp_usr)

    ctx = {
        "group": grp,
        'group_pk': pk,
        "tasks": grp_tsk,
        'users': grp_usr,
        'grp_tsk_len': grp_tsk_len,
        'grp_usr_len': grp_usr_len,
    }
    return render(request, "group.html", context = ctx)
   

def create_group(request):
    # Provide Group creation page
    if request.method == "GET":
        context = {
            "form": GroupForm(),
        }
        return render(request, 'group_create.html', context = context)
        
    # Handle group creation
    if request.method == "POST":
        grp_frm = GroupForm(request.POST)

        if grp_frm.is_valid():
            grp = grp_frm.save()
            Belongs.objects.create(user = request.user, group = grp)
            print("group_create - Group was successfully created")
            return redirect("group_list_view")
        else:
            err_msg = 'Failed to create group'
            log_and_raise_exception(err_msg)

def delete_group(request, pk):
    """
    Function designed to handle delete requests for group at specified kek
    """
    grp = get_group_by_id(pk)
    grp.delete()

    return redirect("group_list_view")


