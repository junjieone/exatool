# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from foo.forms import *
from subprocess import Popen, PIPE
import jinja2

# Create your views here.
def execute(request):
    if request.method == "POST":
        form = ParamForm(request.POST)
        if form.is_valid():
            template_path = './foo/files/template.j2'
            conf_path = '../../lab/exabgp/vpn.conf'
            conf = ""
            with open(template_path, 'r') as f:
                template = jinja2.Template(f.read())
                conf = template.render(params=form.cleaned_data)
                f.close()
            with open(conf_path, 'w') as f:
                f.write(conf)
                f.close()
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm': paramForm, 'response':conf})
    else:
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm':paramForm})
