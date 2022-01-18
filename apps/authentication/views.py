# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
import hashlib
import sys
import traceback
from django.core.mail import get_connection, EmailMultiAlternatives
from apps.home.models import User
from apps.home.views import index

def siginin(request):
    return render(request, "accounts/login.html")

def login_user(request):
    usermail = request.POST.get('usermail')
    userpass = request.POST.get('userpass')
    remember_me = request.POST.get('rememberme')
    captcha = request.POST.get('g-recaptcha-response')
    print("captcha:::", captcha)
    print("remember_me:::", remember_me)

    auth_res = authenticate(request, correo_personal=usermail, password=userpass)
    if auth_res is not None:
        login(request, auth_res)
        if remember_me == 0:
            request.session.set_expiry(0)
        # return JsonResponse({'status': 'ok'})
        return redirect(index)
    else:
        return redirect(siginin)

def register_user(request):
    username = request.POST.get("username")
    usermail = request.POST.get("usermail")
    userpass = request.POST.get("userpass")
    
    # checking same email already exist
    user = User.objects.filter(correo_personal=usermail)
    if len(user) > 0:
        return JsonResponse({'status': 'duplicate'})    

    user = User(nombres_usuario=username, correo_personal=usermail, password=userpass, role_id=3)
    user.set_password(userpass)
    user.save()

	# authenticating user
    user = authenticate(request, correo_personal=usermail, password=userpass)
    if user is not None:
        login(request, user)
    
    # reloading current url
    return JsonResponse({'status': 'ok'})
    
def signup(request):
    return render(request, "accounts/register.html")

def getlogout(request):
	logout(request)
	return redirect(siginin)

def forgot_password(request):
    return render(request, "home/page-forgot-password.html")

def reset_password_mail(request):
    email = request.POST.get('email')
    hashval = hashlib.md5(email.encode())
    hashString = str(hashval.hexdigest())
    domain = request.META['HTTP_HOST']
    link = "http://" + domain + "/forgot_password/" + hashString

    try:
        obj = User.objects.get(correo_personal=email)
        if obj is not None:
            obj.hash = hashString
            obj.save()

            connection = get_connection()  # uses SMTP server specified in settings.py
            connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()
            imageLink = f"https://booctep.herokuapp.com/static/assets/img/favicon.png"
            text = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
            text += '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">'
            text += '<head><!--[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]--><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="x-apple-disable-message-reformatting"><!--[if !mso]><!-->'
            text += '<meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]--><title></title><style type="text/css">table, td { color: #000000; } a { color: #0000ee; text-decoration: underline; } @media (max-width: 480px) { #u_content_button_4 .v-padding { padding: 20px 50px !important; } }'
            text += '@media only screen and (min-width: 620px) {.u-row { width: 600px !important;}.u-row .u-col {vertical-align: top;}.u-row .u-col-100 {width: 600px !important;}}'
            text += '@media (max-width: 620px) {.u-row-container {max-width: 100% !important;padding-left: 0px !important;padding-right: 0px !important;}.u-row .u-col {min-width: 320px !important;max-width: 100% !important;display: block !important;}'
            text += '.u-row {width: calc(100% - 40px) !important;}.u-col {width: 100% !important;}.u-col > div {margin: 0 auto;}}body {margin: 0;padding: 0;}table,tr,td {vertical-align: top;border-collapse: collapse;}p {margin: 0;}'
            text += '.ie-container table,.mso-container table {table-layout: fixed;}* {line-height: inherit;}a[x-apple-data-detectors="true"] {color: inherit !important;text-decoration: none !important;}</style>'
            text += '<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Lato:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap" rel="stylesheet" type="text/css"><link href="https://fonts.googleapis.com/css?family=Raleway:400,700&display=swap" rel="stylesheet" type="text/css"><!--<![endif]--></head>'
            text += '<body class="clean-body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #efefef;color: #000000"><!--[if IE]><div class="ie-container"><![endif]--><!--[if mso]><div class="mso-container"><![endif]--><table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #efefef;width:100%" cellpadding="0" cellspacing="0"><tbody><tr style="vertical-align: top"><td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top"><!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #efefef;"><![endif]--><div class="u-row-container" style="padding: 0px;background-color: transparent"><div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color:   #d7dbf5;"><div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;"><!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: #0000ff;"><![endif]--><!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]--><div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;"><div style="width: 100% !important;"><!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->'
            text += '<table style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"><tbody><tr><td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:Open Sans,sans-serif;" align="left"><table width="100%" cellpadding="0" cellspacing="0" border="0" ><tr>'
            text += '<td style="padding-right: 0px;padding-left: 0px;" align="center"><img align="center" border="0" src="{imageLink}" alt="Image" title="Image" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 80px;" width="80">'
            text += '</td></tr></table></td></tr></tbody></table><!--[if (!mso)&(!IE)]><!--></div><!--<![endif]--></div></div><!--[if (mso)|(IE)]></td><![endif]--><!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]--></div></div></div>'
            text += '<div class="u-row-container" style="padding: 0px;background-color: transparent"><div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"><div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">'
            text += '<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: #ffffff;"><![endif]--><!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]--><div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;"><div style="width: 100% !important;"><!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]--><table style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0" >'
            text += '<tbody><tr><td style="overflow-wrap:break-word;word-break:break-word;padding:18px 10px 12px;font-family:Open Sans,sans-serif;" align="left"><div style="color: #333333; line-height: 140%; text-align: center; word-wrap: break-word;"><p style="font-size: 14px; line-height: 140%;">'
            text += '<span style="font-size: 22px; line-height: 30.8px;"><strong>إعادة تعيين كلمة المرور</strong></span></p></div></td></tr></tbody></table><!--[if (!mso)&(!IE)]><!--></div><!--<![endif]--></div></div><!--[if (mso)|(IE)]></td><![endif]--><!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]--></div></div></div><div class="u-row-container" style="padding: 0px;background-color: transparent">'
            text += '<div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"><div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">'
            text += '<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: #ffffff;"><![endif]-->'
            text += '<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]--><div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;"><div style="width: 100% !important;"><!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]-->'
            text += '<table style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0" ><tbody><tr>'
            text += '<td style="overflow-wrap:break-word;word-break:break-word;padding:0px 25px 10px;font-family:Open Sans,sans-serif;" align="left"><div style="color: #333333; line-height: 160%; text-align: center; word-wrap: break-word;"><p style="font-size: 14px; line-height: 160%; text-align: right;">لإعادة تعيين كلمة المرور, الرجاء الضغط على الرابط بالأسفل</p></div></td></tr></tbody></table><!--[if (!mso)&(!IE)]><!--></div><!--<![endif]--></div></div><!--[if (mso)|(IE)]></td><![endif]--><!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]--></div></div></div><div class="u-row-container" style="padding: 0px;background-color: transparent"><div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"><div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">'
            text += '<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: #ffffff;"><![endif]-->'
            text += '<!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]-->'
            text += '<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;"><div style="width: 100% !important;"><!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;"><!--<![endif]--><table id="u_content_button_4" style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"><tbody><tr><td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:Open Sans,sans-serif;" align="left"><div align="center"><!--[if mso]><table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-spacing: 0; border-collapse: collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;font-family:Open Sans,sans-serif;"><tr><td style="font-family:Open Sans,sans-serif;" align="center"><v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="" style="height:38px; v-text-anchor:middle; width:274px;" arcsize="92%" stroke="f" fillcolor="#1b36ab"><w:anchorlock/><center style="color:#FFFFFF;font-family:Open Sans,sans-serif;"><![endif]-->'
            text += '<a href="' + link + '" target="_blank" style="box-sizing: border-box;display: inline-block;font-family:Open Sans,sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #33BEFF; border-radius: 35px; -webkit-border-radius: 35px; -moz-border-radius: 35px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;"><span class="v-padding" style="display:block;padding:12px 40px 10px;line-height:120%;"><span style="font-size: 14px; line-height: 16.8px;"><strong><span style="line-height: 16.8px; font-size: 14px;"> تغيير كلمة المرور</span></strong></span></span></a><!--[if mso]></center></v:roundrect></td></tr></table><![endif]--></div></td></tr></tbody></table>'
            text += '<!--[if (!mso)&(!IE)]><!--></div><!--<![endif]--></div></div><!--[if (mso)|(IE)]></td><![endif]--><!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]--></div></div></div><div class="u-row-container" style="padding: 0px;background-color: transparent"><div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;"><div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">'
            text += '<!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr style="background-color: #ffffff;"><![endif]--><!--[if (mso)|(IE)]><td align="center" width="600" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;" valign="top"><![endif]--><div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;"><div style="width: 100% !important;"><!--[if (!mso)&(!IE)]><!-->'
            text += '<div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;">'
            text += '<!--<![endif]--><table style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0"><tbody><tr><td style="overflow-wrap:break-word;word-break:break-word;padding:15px 10px 9px;font-family:Open Sans,sans-serif;" align="left">'
            text += '<table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="72%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #DFF2F5;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%"><tbody><tr style="vertical-align: top">'
            text += '<td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">'
            text += '<span>&#160;</span></td></tr></tbody></table></td></tr></tbody></table><table style="font-family:Open Sans,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">'
            text += '<tbody><tr><td style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:Open Sans,sans-serif;" align="left"><div style="color: #7e7e81; line-height: 150%; text-align: center; word-wrap: break-word;"><p style="font-size: 14px; line-height: 150%;">'
            text += '<span style="font-size: 12px; line-height: 18px;">هذه الرسالة تلقائية من فريق دعم منصة بوستيب, نتمنى لك يوما سعيد</span><span style="font-size: 12px; line-height: 18px;"></span>'
            text += '</p></div></td></tr></tbody></table><!--[if (!mso)&(!IE)]><!--></div><!--<![endif]--></div></div><!--[if (mso)|(IE)]></td><![endif]--><!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]--></div></div></div><!--[if (mso)|(IE)]></td></tr></table><![endif]--></td></tr></tbody></table><!--[if mso]></div><![endif]--><!--[if IE]></div><![endif]--></body></html>'

            to = email
            subject = 'Reset password request'

            msg = EmailMultiAlternatives(subject, '...', 'support@booctep.com', [to])
            msg.attach_alternative(text, "text/html")
            msg.send()

        else:
            msg = 'error'
            hashString = "0"
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        msg = tbinfo + "\n" + ": " + str(sys.exc_info())
        hashString = "0"

    return HttpResponse("We have sent email for link to your email.")

def reset_password(request, hashval):   
    return render(request, 'home/page-reset-password.html')

def change_password(request):
    hashval = request.POST.get('hashval')
    u = User.objects.get(hash=hashval)
    if u is not None:
        newpassword = request.POST.get('password')
        u.set_password(newpassword)
        u.save()

        status = 'ok'
    else:
        status = 'fail'
    return redirect(siginin)