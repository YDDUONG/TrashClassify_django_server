from django.shortcuts import redirect, render
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from trash import forms
from django.http import HttpResponse
from trash import models
import time

def review(request):
    if request.method=='POST':
        request.session['is_back'] = False
        message = None
        if request.POST.get('edit_id_submit',None):
            try:
                trash_review = models.edit_history.objects.get(id=request.POST.get('edit_id_submit',None))
                id = request.POST.get('userid',None)
                if str(trash_review.method)=="add":
                    try:
                        models.trash.objects.create(name=trash_review.name,mtype=int(trash_review.mtype),modify1=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                        models.edit_history.objects.filter(id=int(request.POST.get('edit_id_submit',None))).delete()
                    except:
                        message = "该垃圾已存在于数据库中,请勿重复添加.点击\"审核不通过\"按钮撤销改修改请求"
                elif str(trash_review.method)=="modify":
                    trash = models.trash.objects.filter(name=trash_review.name)
                    trash1 = models.trash.objects.get(name=trash_review.name)
                    try:
                        if(len(trash1.modify1)<10):
                            trash.update(modify1=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                            models.edit_history.objects.filter(id=int(request.POST.get('edit_id_submit',None))).delete()
                            message = "修改成功(第一次修改)"
                        elif(len(trash1.modify2)<10):
                            trash.update(modify2=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                            models.edit_history.objects.filter(id=int(request.POST.get('edit_id_submit',None))).delete()
                            message = "修改成功(第二次修改)"
                        elif(len(trash1.modify3)<10):
                            trash.update(modify3=str(id)+str(time.strftime("%Y%m%d%H%M%S", time.localtime())))
                            models.edit_history.objects.filter(id=int(request.POST.get('edit_id_submit',None))).delete()
                            message = "修改成功(第三次修改)"
                        else:
                            message = "该垃圾修改次数已达上限(三次修改),改垃圾词条被锁定,如有需要请上报管理员进行修改.点击\"审核不通过\"按钮撤销改修改请求"
                    except:
                        message = "该垃圾不存在于数据库中,不能完成修改请求.点击\"审核不通过\"按钮撤销改修改请求"
                else:
                    message = "数据传输可能出现错误,请点击\"审核不通过\"按钮撤销改修改请求"
            except:
                message = "该垃圾不存在于数据库中,不能完成修改请求.点击\"审核不通过\"按钮撤销改修改请求"
        elif request.POST.get('edit_id_delete',None):
            try:
                models.edit_history.objects.filter(id=int(request.POST.get('edit_id_delete',None))).delete()
                message = "删除成功"
            except:
                message = "删除失败,请上报改错误给管理员"
        else:
            message = "数据传输可能出现错误,请点击\"审核不通过\"按钮撤销改修改请求"
    wait_review = models.edit_history.objects.filter()
    return render(request, 'login/index.html', locals())

def login(request):
    hashkey = CaptchaStore.generate_key()  
    image_url = captcha_image_url(hashkey)
    if request.session.get('is_login',None):
        return redirect('/review_index')

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            valid_hashkey = login_form.cleaned_data['hashkey']
            valid = CaptchaStore.objects.get(hashkey=valid_hashkey)
            captcha = login_form.cleaned_data['captcha']
            if str.lower(captcha) == str.lower(str(valid)):
                try:
                    user = models.user_info.objects.get(email=email)
                    if user.password == password:
                        request.session['is_login'] = True
                        request.session['is_back'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.email
                        return redirect("/review_index/")
                    else:
                        message = "用户名或密码不正确！"
                except:
                    message = "用户不存在"
            else:
                message = "验证码不正确！"

    login_form = forms.UserForm()
    return render(request, "login/login.html", locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/review_index/")
    request.session.flush()
    return redirect("/review_index/")