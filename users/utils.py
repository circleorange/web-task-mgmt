from core.utils import log_and_raise_exception
from users.models import CustomUser


def get_user_by_id(usr_pk):
    try:
        return CustomUser.objects.get(id = usr_pk)
    except:
        err_msg = 'Failed to retrieve user by ID'
        log_and_raise_exception(err_msg)


def is_valid_user_by_email(eml):
    """
    Check whether user email address exists in the database
    """
    if eml is None:
        return False

    if CustomUser.objects.filter(email = eml).exists():
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
            err_msg = 'Failed to retrieve user by email'
            log_and_raise_exception(err_msg)
    else:
        err_msg = 'User not found'
        log_and_raise_exception(err_msg)
