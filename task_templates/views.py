from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import TaskTemplate
from .forms import TaskTemplateForm, TemplateFieldForm

def template_view(req):
    tmp_frm = TaskTemplateForm()
    tmp_fld_frm = TemplateFieldForm()
    return render(req, 'tmp.html', {'tmp': tmp_frm, 'tmp_fld': tmp_fld_frm})


def create_template(req):
    if req.method == 'POST':
        tmp_frm = TaskTemplateForm(req.POST)
        tmp_fld_frm = TemplateFieldForm(req.POST)
        if tmp_frm.is_valid() and tmp_fld_frm.is_valid():
            tmp = tmp_frm.save()
            for frm in tmp_fld_frm:
                fld = frm.save(commit=False)
                fld.template = tmp
                fld.save()
            return redirect('template_list')
    
    return render(req, 'tmp.html', {'tmp': tmp_frm, 'tmp_fld': tmp_fld_frm})


def task_input_form(request, template_id):
    template = TaskTemplate.objects.get(id=template_id)
    fields = template.templatefield_set.all()
    return render(request, 'task_input_form.html', {'template': template, 'fields': fields})
