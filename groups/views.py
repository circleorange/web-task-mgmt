import traceback
from django.shortcuts import get_object_or_404, redirect, render

from users.models import CustomUser
from groups.models import Group
from .forms import GroupForm

def groups_view(request):
    context = {}
    try:
        group_list = request.user.user_groups.all()

        context = {
            "groups": group_list
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
    if request.method == "GET":
        try:
            context = {
                "group": get_object_or_404(Group, pk = pk)
            }
            print(f"group_get - Group was succesfully retrieved: {pk}")
            return render(request, "group.html", context)
        except:
            print("group_get - Failed to retrieve group")
            traceback.print_exc()


def group_create(request):
    if request.method == "GET":
        try:
            # retrieve the group form and respond to client
            context = {
                "form": GroupForm(),
            }
            return render(request, "group_create.html", context)
        except:
            traceback.print_exc()
    
    if request.method == "POST":
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            group = group_form.save()
            group.users.add(request.user)

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

