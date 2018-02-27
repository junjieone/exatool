# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from foo.forms import *
from subprocess import Popen, PIPE
import jinja2
import paramiko #apt-get install python-dev; install PyCrypto; then paramiko

# Create your views here.
def generate(request):
    form = ParamForm(request.POST)
    if form.is_valid():
        template_path = './foo/files/template.j2'
        conf = ""

        # check loop
        prefix = form.cleaned_data['is_pref']
        is_prefs = prefix.split(',')

        with open(template_path, 'r') as f:
            template = jinja2.Template(f.read())
            conf = template.render(params=form.cleaned_data, is_prefs = is_prefs)
            f.close()

        final_conf = ""
        for line in conf.splitlines():
            if line.split():
                final_conf += line + "\n"

        paramForm = ParamForm()
    return render(request, "execute.html", {'paramForm': paramForm, 'conf':final_conf})
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

@csrf_exempt
def command(request):
    hostname = '172.27.10.79'
    username = 'lab'
    password = 'lab123'
    execmd = request.POST['cmd']

    response = sshclient_execmd(hostname, username, password, execmd)
    response = response.decode(encoding="utf-8")
    return JsonResponse({'output': response})

def sshclient_execmd(hostname, username, password, execmd):
    response = ""
    #paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = s.exec_command(execmd)
    #stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    response = stdout.read()
    s.close()
    return response
