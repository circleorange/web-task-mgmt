from django.shortcuts import render

def task_list_view(req):
    print("taskListView.request")
    return render(req, "task_list.html")

def task_template_view(req):
    print("templateView.request")
    return render(req, "task_template.html")