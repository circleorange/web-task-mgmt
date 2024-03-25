from django.forms import formset_factory
from django.shortcuts import render

from django.shortcuts import render, redirect
from .models import TaskTemplate, TemplateField
from .forms import TaskTemplateForm, TemplateFieldForm

def template_view(req):
    tmp_frm = TaskTemplateForm()
    tmp_fld_frm = TemplateFieldForm()
    return render(req, 'tmp.html', {'tmp': tmp_frm, 'tmp_fld': tmp_fld_frm})


def create_template(req):
    print('create-template - request')
    if req.method != "POST": return render(req, "tmp.html")
    print('create-template - request POST')

    # use formset to handle multiple instance of TemplateFieldForm
    TemplateFieldFormSet = formset_factory(TemplateFieldForm)

    tmp_frm = TaskTemplateForm(req.POST)
    tmp_fld_frmset = TemplateFieldFormSet(req.POST)

    if tmp_frm.is_valid() and tmp_fld_frmset.is_valid():
        print('create-template - request valid')
        tmp_inst = tmp_frm.save(commit = False)
        tmp_inst.user = req.user
        tmp_inst.save()

        for tmp_fld_frm in tmp_fld_frmset:
            fld_name = tmp_fld_frm.cleaned_data.get('field_name')
            fld_is_req = tmp_fld_frm.cleaned_data.get('is_required')
            fld_is_inc = tmp_fld_frm.cleaned_data.get('is_included')
            print(f"{fld_name}, is_required: {fld_is_req}, is_included: {fld_is_inc}")

            if fld_name:
                print('create-template - request processing fields')
                TemplateField.objects.create(
                    template = tmp_inst,
                    field_name = fld_name,
                    is_required = fld_is_req,
                    is_included = fld_is_inc,
                )
        return redirect(req, 'task_list')
    else:
        print('create-template - request invalid')



def task_input_form(request, template_id):
    template = TaskTemplate.objects.get(id=template_id)
    fields = template.templatefield_set.all()
    return render(request, 'task_input_form.html', {'template': template, 'fields': fields})
