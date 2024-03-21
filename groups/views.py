from django.http import HttpResponse
from django.shortcuts import redirect, render
from core.models import Belongs
from groups.utils import *
from tasks.utils import get_task_by_id
from users.utils import *
from tasks.forms import TaskForm
from tasks.models import Task

from .forms import GroupForm


def get_group_description(req, grp_pk):
    grp = get_group_by_id(grp_pk)
    ctx = {
        'group': grp,
    }
    return render(req, 'grp_desc_field.html', ctx)


def set_group_description(req, grp_pk):
    if req.method == "GET":
        grp = get_group_by_id(grp_pk)
        ctx = {
            'group': grp,
        }
        return render(req, 'grp_desc_input.html', ctx)

    if req.method == "POST":
        grp_desc = req.POST.get('description')
        grp = get_group_by_id(grp_pk)
        grp.description = grp_desc
        grp.save()

        ctx = {
            'group': grp,
        }
        return render(req, 'grp_desc_field.html', ctx)


def update_group_task(request, grp_pk, tsk_pk):
    tsk = get_task_by_id(tsk_pk)
    frm = TaskForm(request.POST, instance = tsk)
    if frm.is_valid(): frm.save()

    return group_detail_view(request, grp_pk)


def remove_user_from_group(request, grp_pk, usr_pk):
    grp = get_group_by_id(grp_pk)
    usr = get_user_by_id(usr_pk)

    try:
        Belongs.objects.filter(user = usr, group = grp).delete()
    except:
        err_msg = 'Failed to remove user from group'
        log_and_raise_exception(err_msg)
    
    return group_detail_view(request, grp_pk)


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
        return group_detail_view(request, pk)
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
    grp = get_group_by_id(pk)
    grp_tsk = get_tasks_by_group(grp)
    grp_usr = get_users_by_group(grp)

    usr_id = request.user.id
    usr = get_user_by_id(usr_id)
    # user group role
    usr_grp_role = get_user_role(grp, usr)
    # control group permissions if user has sufficient role
    grp_admin_perm = True if usr_grp_role == 'Leader' else False

    grp_tsk_len = len(grp_tsk)
    grp_usr_len = len(grp_usr)

    ctx = {
        "group": grp,
        'group_pk': pk,
        "tasks": grp_tsk,
        'users': grp_usr,
        'grp_tsk_len': grp_tsk_len,
        'grp_usr_len': grp_usr_len,
        'grp_admin_perm': grp_admin_perm,
    }
    return render(request, "group.html", context = ctx)
   

def create_group(request):
    if request.method == "GET":
        context = {
            "form": GroupForm(),
        }
        return render(request, 'group_create.html', context = context)
        
    if request.method == "POST":
        grp_frm = GroupForm(request.POST)

        if grp_frm.is_valid():
            grp = grp_frm.save()
            Belongs.objects.create(user = request.user, group = grp, role = Belongs.Role.LEADER)
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


