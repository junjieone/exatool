# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from foo.forms import *
from subprocess import Popen, PIPE
import os,sys
import jinja2
import paramiko #apt-get install python-dev; install PyCrypto; then paramiko


conf_path = '../../lab/exabgp/vpn.conf'
cmd_j2 = './foo/files/commands.j2'

# Create your views here.
def generate(request):
    form = ParamForm(request.POST)
    if form.is_valid():
        template_path = './foo/files/template.j2'
        conf = ""

        '''
        # check loop
        prefix = form.cleaned_data['is_pref']
        is_prefs = prefix.split(',')

        with open(template_path, 'r') as f:
            template = jinja2.Template(f.read())
            conf = template.render(params=form.cleaned_data, is_prefs = is_prefs)
            f.close()
        '''

        with open(template_path, 'r') as f:
            template = jinja2.Template(f.read())
            conf = template.render(params=form.cleaned_data)
            f.close()
        final_conf = ""
        for line in conf.splitlines():
            if line.split():
                final_conf += line + "\n"
    return JsonResponse({'conf':final_conf})

@csrf_exempt
def create(request):
    global conf_path
    vpn_conf = request.POST['vpn_conf']
    #conf_path = conf_path.decode(encoding="utf-8")
    with open(conf_path, 'w') as f:
        f.write(vpn_conf)
        f.close()
    return JsonResponse({})

def execute(request):
    '''
    if request.method == "POST":
        conf = request.POST['conf']
        conf_path = '../../lab/exabgp/vpn.conf'
        conf_path = conf_path.decode(encoding="utf-8")
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
    '''
    paramForm = ParamForm()
    return render(request, "execute.html", {'paramForm':paramForm})

@csrf_exempt
def command(request, action, category="", operation=""):
    global conf_path
    if action == 'start':
        cmd = "exabgp %s" % (conf_path)
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result = ""
        count = 0 #Temporarily solve the unstop 'exabgp' running
        for i in iter(process.stdout.readline, 'b'):
            result = result + i.decode(encoding="utf-8")
            count = count + 1
            if count == 100:
                break
        return JsonResponse({'result': result, 'action': action})
    if action == 'modify':
        with open(cmd_j2, 'r') as f:
            params = {}
            template = jinja2.Template(f.read())
            params['category'] = category
            params['operation'] = operation
            for k in request.POST.keys():
                params[k] = request.POST[k]
            cmd = template.render(params).strip() #Get the command and eliminate blank lines
            f.close()
        '''
        if category == 'normal':
            nm_nb_addr = request.POST['nm_nb_addr']
            nm_pref = request.POST['nm_pref']
            nm_nh = request.POST['nm_nh']
            if operation == 'announce':
                cmd = 'curl --form "command=neighbor '+nm_nb_addr+ ' announce route '+nm_pref+' next-hop '+nm_nh+'" http://localhost:5001/announce route '+nm_pref+' next-hop '+nm_nh+' &'
            if operation == 'withdraw':
                cmd = 'curl --form "command=neighbor '+nm_nb_addr+ ' withdraw route '+nm_pref+' next-hop '+nm_nh+'" http://localhost:5001/withdraw route '+nm_pref+' next-hop '+nm_nh+' &'
        if category == 'label':
            lb_nb_addr = request.POST['nm_nb_addr']
            lb_pref = request.POST['lb_pref']
            lb_nh = request.POST['lb_nh']
            lb_lb = request.POST['lb_lb']
            if operation == 'announce':
                cmd = 'curl - -form "command=neighbor '+lb_nb_addr+' announce route '+lb_pref+' next-hop '+lb_nh+' label '+lb_lb+'" http://localhost:5001/neighbor '+lb_nb_addr+' announce route '+lb_pref+' next-hop 100.100.100.4 label '+lb_lb+' &'
            if operation == 'withdraw':
                cmd = 'curl - -form "command=neighbor '+lb_nb_addr+' withdraw route '+lb_pref+' next-hop '+lb_nh+' label '+lb_lb+'" http://localhost:5001/neighbor '+lb_nb_addr+' withdraw route '+lb_pref+' next-hop 100.100.100.4 label '+lb_lb+' &'
        if category == 'flowspec':
            fs_nb_addr = request.POST['fs_nb_addr']
            fs_sr_pref = request.POST['fs_sr_pref']
            fs_dt_nh = request.POST['fs_dt_nh']
            fs_act = request.POST['fs_act']
            if operation == 'announce':
                return
        '''
    if action == 'terminate':
        cmd_getTID = "pgrep exabgp"
        tid = local_execmd(cmd_getTID).decode(encoding="utf-8")
        cmd = "kill " + tid

        #Execute the command
        result = local_execmd(cmd)
        result = result.decode(encoding="utf-8")
        return JsonResponse({'result': result, 'action':action})

def collect(request):
    if request.method == "POST":
        form = CollectForm(request.POST)
        if form.is_valid():
            hostname = form.cleaned_data['hostname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            execmd = form.cleaned_data['command'].strip()

            response = sshclient_execmd(hostname, username, password, execmd)
            response = response.decode(encoding="utf-8")
            return JsonResponse({'response': response, 'hostname': hostname})
    else:
        collectForm = CollectForm()
        return render(request, "collect.html", {'collectForm': collectForm})

def local_execmd(cmd):
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if stdout.decode(encoding="utf-8") == "":
        result = stderr
    else:
        result = stdout
    return result

def sshclient_execmd(hostname, username, password, execmd):
    #paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = s.exec_command(execmd)
    #stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
    response = stdout.read()
    s.close()
    return response
