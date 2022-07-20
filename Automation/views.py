from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from Automation.models import *
from Automation.User_form import user_form,function_form,case_form
from Automation.FunctionMan import FunctionMy
from django.core import serializers
import json
from Automation.CaseSync import *
import os
from os import path
# Create your views here.
def login(request):
    # python manage.py createsuperuser
    if request.method=='GET':
        return render(request,"login.html")
    else:
        print(request.POST)
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        next  = request.GET.get('next','/index/')
        reponse = {"user":None,"msg":"","url":next}
        user = auth.authenticate(username=name,password=pwd)
        if user:
            user_obj = UserAuto.objects.filter(username=name).first()
            if user_obj.authen:
                auth.login(user=user,request=request)
                reponse['user'] = user.username
            else:
                reponse["msg"] = '请等待管理审核'
        else:
            user_obj = UserAuto.objects.filter(username=name).first()

            if user_obj:
                reponse["msg"]='用户名或密码错误'
            else:
                reponse["msg"] = '不存在该用户'
        print(reponse)
        return JsonResponse(reponse)
@login_required
def index(request):
    projext_val = request.GET.get('project')
    form = function_form()
    if projext_val:
        Function_list = Function.objects.filter(project__nid=projext_val).values_list('name', 'project__name', 'user__username',
                                                           Count('feature__case'),'nid')
    else:
        Function_list = Function.objects.all().values_list('name','project__name','user__username',Count('feature__case'),'nid')
    Projext_list = Project.objects.all()
    return render(request,'index.html',locals())

def reg(request):
    if request.method=='POST':

        form = user_form(request.POST)
        response={"user":None,"msg":{}}
        if form.is_valid():
            response['user'] = form.cleaned_data.get('name')
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            tel = form.cleaned_data.get('tel')
            print("name",name)
            print("clean",form.cleaned_data)
            UserAuto.objects.create_user(username=name,password=pwd,email=email,telephone=tel)
        else:
            response['msg'] = form.errors

        return JsonResponse(response)
    else:
        form = user_form()
    return render(request, "reg.html", locals())

def manage_user(request):
    User_Unauth = UserAuto.objects.filter(authen=0)
    User_Auth = UserAuto.objects.filter(authen=1,is_superuser=0)
    return render(request,"manage.html",locals())

def auth_user(request,id):
    UserAuto.objects.filter(nid=id).update(authen=1)
    return redirect('/manage')
    #return HttpResponse('ok')

def del_user(request,id):
    UserAuto.objects.filter(nid=id).delete()
    return redirect('/manage')
    #return HttpResponse('ok')

def Function_add(request):
    response = FunctionMy.Function_add(request)
    return response
def del_function(request,id):
    FunctionMy.del_function(request,id)
    next = request.GET.get('next')
    return redirect(next)

def featurelist(request):
    function_id = request.POST.get('functionid')
    feature_list = Feature.objects.filter(func__nid=function_id).values_list('name','eng_name','func__user__username',Count('case'),'nid')

    feature_list = list(feature_list)
    print(feature_list)
    return JsonResponse(json.dumps(feature_list),safe=False)
def ajax_handle(data):
    data_handled = serializers.serialize('json',data)
    print({'data':data_handled})
    return JsonResponse(data_handled,safe=False)
def caselist(request):
    if request.method=='POST':
        id = request.POST.get('id')
        case_list = Case.objects.filter(feature__nid=id).values_list('name','desc','status','ID')
        case_list = list(case_list)
        return JsonResponse(json.dumps(case_list),safe=False)
@login_required
def addcase(request,id):
    if request.method=='GET':
        form = case_form()


        ret = Feature.objects.filter(nid=id).values('name','func__name','func__project__name','eng_name','func__eng_name')
        case_obj =Case.objects.filter(feature__nid=id).last()
        if case_obj:
            case_id = case_obj.ID

            case_id_new = case_id.split('-')[0]+'-'+case_id.split('-')[1]+'-'+case_id.split('-')[2]+'-'+str(int(case_id.split('-')[3])+1)
        else:
            case_id_new = ret[0].get('func__project__name')+'-'+ret[0].get('func__eng_name')+'-'+ret[0].get('eng_name')+'-1'
        feature_name = ret[0].get('name')
        func_name = ret[0].get('func__name')
        proj_name = ret[0].get('func__project__name')
        return render(request,'addcase.html',locals())
    else:
        #form = case_form(request.POST)
        print(request.POST)
        case_id = request.POST.get('case_id')
        step_num = request.POST.get('step_num')
        general_keys = ['csrfmiddlewaretoken', 'step_num', 'case_name', 'case_desc', 'case_id', 'feature_id', 'case_status']
        case_detail = {}
        for i in request.POST.keys():
            if i not in general_keys:
                case_detail[i] = request.POST.get(i)
        case_detail_json = json.dumps(case_detail)
        case_detail_obj = Case_Detail.objects.create(desc=case_detail_json,test=0)
        feature_obj = Feature.objects.filter(nid=request.POST.get('feature_id')).first()
        filename='/work/AutoTest/AutoTest/Test_Case/Unit_'+feature_obj.func.eng_name+'_'+feature_obj.func.project.name+'.py'
        case_pbj = Case.objects.create(name=request.POST.get('case_name'),desc=request.POST.get('case_desc'),ID=request.POST.get('case_id'),user=request.user,
                                       status=1,feature=feature_obj,detail=case_detail_obj)
        CaseCreate(case_detail, step_num, case_id,filename,request.POST.get('case_name'))

        return HttpResponse('OK')
def addsds(request):
    if request.method=="POST":
        file_obj = request.FILES.getlist('avartar')
        category = request.POST.get('name')
        for f in file_obj:
            SDS_Content.objects.create(name=f.name.split('.')[1],category=category,content=f)
        return HttpResponse('OK')
    else:
        return render(request,'addsds.html')

def sdslist(request):
    if request.method=='POST':
        sds_obj = SDS_Content.objects.values_list('nid','name','category')
        sds_obj = list(sds_obj)
        return JsonResponse(json.dumps(sds_obj),safe=False)

def addicon(request):
    if request.method=="POST":
        file_obj = request.FILES.getlist('avartar')
        category = request.POST.get('name')
        for f in file_obj:
            print(f.name)
            ICON_Content.objects.create(name=f.name.split('.')[0],category=category,content=f)
        return HttpResponse('OK')
    else:
        return render(request,'addicon.html')

def iconlist(request):
    if request.method=='POST':
        icon_obj = ICON_Content.objects.values_list('nid','name','category','content')
        icon_obj = list(icon_obj)
        return JsonResponse(json.dumps(icon_obj),safe=False)

