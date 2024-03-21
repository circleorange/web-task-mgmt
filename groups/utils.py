from django.shortcuts import get_object_or_404

from core.models import Belongs
from core.utils import log_and_raise_exception
from groups.models import Group
from tasks.models import Task
from users.models import CustomUser

def get_user_role(grp: Group, usr: CustomUser):
    try:
        return Belongs.objects.get(group = grp, user = usr).role
    except:
        err_msg = "Failed to retrieve user role"
        log_and_raise_exception(err_msg)


def set_user_role(grp: Group, usr: CustomUser, role):
    try:
        relation = Belongs.objects.get(group = grp, user = usr)
        relation.role = role
        relation.save()
    except:
        err_msg = 'Failed to set user role'
        log_and_raise_exception(err_msg)


def get_group_id_by_task(tsk: Task):
    grp: Group = get_group_by_task(tsk)
    return grp.pk


def get_group_by_task(tsk: Task):
    try:
        return get_group_by_id(tsk.group.pk)
    except:
        err_msg = 'Failed to retrieve group by task'
        log_and_raise_exception(err_msg)


def get_users_by_group(grp: Group):
    try:
        grp_usr = Belongs.objects.filter(group = grp)
        grp_usr_lst = [relation.user for relation in grp_usr]
        return grp_usr_lst
    except:
        err_msg = 'Failed to retrieve group members'
        log_and_raise_exception(err_msg)
    

def get_tasks_by_group(grp: Group):
    try:
        return grp.tasks.all()
    except:
        err_msg = 'Failed to retrieve group tasks'
        log_and_raise_exception(err_msg)


def get_groups_by_user(usr: CustomUser):
    try:
        usr_grps = Belongs.objects.filter(user = usr)
        usr_grps_lst = [relation.group for relation in usr_grps]
        return usr_grps_lst
    except:
        err_msg_usr_grp = 'Failed to retrieve user groups'
        log_and_raise_exception(err_msg_usr_grp)


def get_group_by_id(grp_pk):
    """
    Get group by primary key
    """
    try:
        return get_object_or_404(Group, pk = grp_pk)
    except:
        err_msg = 'Failed to retrieve group by ID'
        log_and_raise_exception(err_msg)


def is_user_already_member(req_usr, req_grp):
    """
    Returns True if user is already member of the group
    """
    if Belongs.objects.filter(user = req_usr, group = req_grp):
        return True
    
    return False
