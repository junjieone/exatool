# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from foo.forms import *
from subprocess import Popen, PIPE
import jinja2

# Create your views here.
def generate(request):
    form = ParamForm(request.POST)
    if form.is_valid():
        template_path = './foo/files/template.j2'
        conf = ""
        with open(template_path, 'r') as f:
            template = jinja2.Template(f.read())
            conf = template.render(params=form.cleaned_data)
            f.close()
        paramForm = ParamForm()
    return render(request, "execute.html", {'paramForm': paramForm, 'conf':conf})
def execute(request):
    if request.method == "POST":
        conf = request.POST['conf']
        conf_path = '../../lab/exabgp/vpn.conf'
        with open(conf_path, 'w') as f:
            f.write(conf)
            f.close()

        command = "exabgp %s" % (conf_path)
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stdout == "":
            result = stderr
        else:
            result = stdout
        result = result.decode(encoding="utf-8")
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm': paramForm, 'result':result})
    else:
        paramForm = ParamForm()
        return render(request, "execute.html", {'paramForm':paramForm})
