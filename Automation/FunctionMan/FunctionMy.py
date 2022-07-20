from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from Automation.models import *
from Automation.User_form import user_form,function_form
import os
def Function_add(request):
    if request.is_ajax():
        function_form_obj = function_form(request.POST)
        print(request.POST)
        project = request.POST.get('project')

        response = {'ret':False,'msg':None}
        if function_form_obj.is_valid():
            print(function_form_obj.cleaned_data.get('name'))
            function_obj = Function.objects.filter(name=function_form_obj.cleaned_data.get('name'), project__name=project).first()
            if function_obj:
                response['msg'] = {'all':['该项目下已经有对应模块，请确认']}
            else:
                response['ret'] = True
                project_obj = Project.objects.filter(name=project).first()
                user_obj = UserAuto.objects.filter(username=request.user.username).first()
                function_obj_add = Function.objects.create(name=function_form_obj.cleaned_data.get('name'), eng_name=function_form_obj.cleaned_data.get('eng_name'), project=project_obj)
                function_obj_add.user.add(user_obj)
                filename = '/work/AutoTest/AutoTest/Test_Case/Unit_'+function_form_obj.cleaned_data.get('eng_name')+'_'+project+'.py'
                with open(filename, 'w') as f:
                    Init_File(f,filename)
        else:
            response['msg'] = function_form_obj.errors


        return JsonResponse(response)
def del_function(request,id):
    Function_obj = Function.objects.filter(nid=id).first()
    print(Function_obj.project.name)
    os.remove('/work/AutoTest/AutoTest/Test_Case/Unit_'+Function_obj.eng_name+'_'+Function_obj.project.name+'.py')
    Function.objects.filter(nid=id).delete()

def Init_File(f,filename):
    f.write('import time\n')
    f.write('from main import *\n')
    f.write('global Test_Util1\n')
    f.write('class %s (unittest.TestCase):\n' %filename)