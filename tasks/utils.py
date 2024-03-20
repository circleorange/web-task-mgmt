from core.utils import log_and_raise_exception
from groups.models import Group
from tasks.models import Task
from users.models import CustomUser


def get_task_by_id(tsk_pk):
    try:
        return Task.objects.get(pk = tsk_pk)
    except:
        err_msg = 'Failed to retrieve task by ID'
        log_and_raise_exception(err_msg)


def get_all_tasks():
    try:
        return Task.objects.all()
    except:
        err_msg = 'Failed to retrieve all tasks'
        log_and_raise_exception(err_msg)


def get_tasks_by_user(usr: CustomUser):
    try:
        return Task.objects.get(user = usr.pk)
    except:
        err_msg = 'Failed to retrieve tasks by user'
        log_and_raise_exception(err_msg)


def get_tasks_by_user_id(usr_pk):
    try:
        return Task.objects.filter(user = usr_pk)
    except:
        err_msg = 'Failed to retrieve tasks by user ID'
        log_and_raise_exception(err_msg)


def is_group_task(tsk: Task):
    if tsk.group.pk is not None:
        if Group.objects.filter(pk = tsk.group.pk).exists():
            return True

    return False
