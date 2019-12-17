from django.shortcuts import render,redirect
from django.http import HttpResponse
from trash import models
import time
from django.contrib.gis import serializers
from django.http.response import JsonResponse


def signin(request):
    if request.method == "POST":
        id = request.POST.get('id',None)
        password = request.POST.get('password',None)
        email = request.POST.get('email',None)
        if (id or email) and password:
            if id:
                try:
                    user = models.user_info.objects.get(id=id)
                    if user.password==password:
                        return HttpResponse("success+"+str(user.email))
                    else:
                        return HttpResponse("password error")
                except:
                    return HttpResponse("no such user")
            if email:
                try:
                    user = models.user_info.objects.get(email=email)
                    if user.password==password:
                        return HttpResponse("success+"+str(user.id))
                    else:
                        return HttpResponse("password error")
                except:
                    return HttpResponse("no such user")
        else:
            return HttpResponse("error post")
    else:
        return HttpResponse("not post")

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        try:
            models.user_info.objects.get(email=email)
            return HttpResponse("repeat email")
        except:
            new_user = models.user_info.objects.create(email=email,password=password)
            return HttpResponse("success+"+str(new_user.id))
    else:
        return HttpResponse("not post")

def modify(request):
    if request.method == "POST":
        method = request.POST.get('method',None)
        id = request.POST.get('id',None)
        name = request.POST.get('name',None)
        mtype = request.POST.get('mtype',None)
        if(method == "add"):
            try:
                models.trash.objects.create(name=name,mtype=int(mtype),modify1=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                return HttpResponse("success")
            except:
                return HttpResponse("already exist")
        elif(method == "modify"):
            trash = models.trash.objects.filter(name=name)
            trash1 = models.trash.objects.get(name=name)
            try:
                if(len(trash1.modify1)<10):
                    trash.update(modify1=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                    return HttpResponse("success1")
                elif(len(trash1.modify2)<10):
                    trash.update(modify2=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                    return HttpResponse("success2")
                elif(len(trash1.modify3)<10):
                    trash.update(modify3=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                    return HttpResponse("success3")
                else:
                    return HttpResponse("locked")
            except:
                return HttpResponse("not_exists")
    else:
        return HttpResponse("not post")

def retrive(request):
    try:
        trashes = models.trash.objects.filter()
        r = []
        for trash in trashes:
            if str(trash).split(":")[2] != "None":
                r.append(str(trash)+"&")
        return HttpResponse(r)
    except:
        return HttpResponse("not exist")
    

def update(request):
    if request.method == "POST":
        method = request.POST.get("method",None)
        userid = request.POST.get('userid',None)
        name = request.POST.get("name",None)
        mtype = request.POST.get("mtype",None)
        try:
            models.edit_history.objects.create(
                method = method, userid = userid, name = name, mtype = int(mtype),
                datetime = time.strftime("%Y%m%d%H%M%S", time.localtime()))
            return HttpResponse("success")
        except:
            return HttpResponse("false")