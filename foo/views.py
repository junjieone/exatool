# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from foo.forms import *
import jinja2

# Create your views here.
def execute(request):
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            with open('./foo/files/template.j2', 'r') as f:
                template = jinja2.Template(f.read())
                text = template.render(params=form.cleaned_data)
                print(text)
                f.close()
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm': paramForm, 'response':text})
    else:
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm':paramForm})
