from fileinput import FileInput
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required 
import datetime
import uuid, re
from . tokens import generate_token
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str 
from django.conf import settings
from PharmaPill import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 

from AuthenticApp.models import db_Profile
# from StorePharma.models import db_Profile

# Create your views here.

def logIn(request):
    #template = loader.get_template('account/logIn.html')
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            var_Email = request.POST.get('login-email')
            var_password = request.POST.get('login-password')

            user_obj = User.objects.filter(email = var_Email).first()  
            user = authenticate(username = var_Email , password = var_password) 
            profile_obj = db_Profile.objects.filter(db_email = user_obj ).first() 


            if (len(var_password) >= 6): 
                
                if user_obj is None:
                    messages.error(request, 'User or E-mail not found.')
                    return redirect('lgIn') 
                if user_obj.is_staff: 
                    if user is None:
                        messages.error(request, 'Wrong password.') 
                        return redirect('lgIn')
                    login(request , user) 
                    return redirect('home')
                if not profile_obj.is_verified:
                    messages.error(request, 'User is not verified check your E-mail.')
                    return redirect('lgIn') 
                if user is  None:
                    messages.error(request, 'Wrong password.')
                    return redirect('lgIn') 
                
                login(request , user) 
                return redirect('home')
            else:
                messages.error(request, 'Password Must be six charatcer Long')
            
    context = {}
    return render(request , 'logIn.html', context)
            #return HttpResponse(template.render(context, request))
  
def signUp(request):
    date = str(datetime.date.today()) 
    if request.user.is_authenticated:
        return redirect('home') 
    else:
        if request.method == 'POST':
            var_email = request.POST.get('register-email') 
            var_firstName = request.POST.get('register-fname')
            var_lastName = request.POST.get('register-lname')
            var_password = request.POST.get('register-password')
            var_ConfirmPassword = request.POST.get('Conf-register-password')
            var_Gender = request.POST.get('register_Gender')
            var_phoneNumber = request.POST.get('register-phoneNumber')
            var_address = request.POST.get('register-address')
            var_address_Country = request.POST.get('register-address-Country')
            var_date_DoB = request.POST.get('register-DoB')

            var_photo = "/Profile/defaultDP.png"

            if var_date_DoB > date :
                messages.error(request,"Date must be before present date.")
                return redirect('register')
            elif len(var_phoneNumber) >= 14:
                messages.error(request,"Phone number Must be under 13 Digits.")
                return redirect('register')
            elif not (len(var_password) >= 6):
                messages.error(request,"Password Must be six charatcer Long")
                return redirect('register')
            else:
                if var_password != var_ConfirmPassword:
                    messages.error(request,"Password Didn't Match")
                    return redirect('register')
            try:
                if User.objects.filter(email = var_email).first():
                    messages.error(request, 'Email is already Taken.')
                    return redirect('register')
                
                if User.objects.filter(username = var_email).first():
                        messages.error(request, 'Username is already Taken.')
                        return redirect('register')
                    
                user_obj = User(username = var_email , email = var_email)
                user_obj.first_name = var_firstName
                user_obj.last_name = var_lastName
                user_obj.set_password(var_password)
                user_obj.save()

                auth_token = str(uuid.uuid4())
                profile_obj = db_Profile.objects.create(db_email = user_obj ,
                auth_token = auth_token, char_email = var_email, db_photo = var_photo, 
                db_gender = var_Gender, db_phoneNumber = var_phoneNumber,
                db_address = var_address, db_address_Country = var_address_Country, db_date_DoB = var_date_DoB
                )

                profile_obj.save() 
                send_mail_after_registration(var_email , auth_token)
                messages.success(request, 'Email Successfully Register. \n We have sent an email to you , \"Please check your mail to Verify\"')
                return redirect('lgIn')
            except Exception as e:
                print(e)
    return render(request=request, template_name="register.html", context={ })


def verify(request , auth_token):
    try:
        profile_obj = db_Profile.objects.filter(auth_token = auth_token).first()
  
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.') 
                return redirect('lgIn')
            
            profile_obj.is_verified = True 
            profile_obj.save() 
            messages.success(request, 'Your account has been verified.')
            return redirect('lgIn')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('lgIn')

def error_page(request):
    return  render(request , 'error.html')

def send_mail_after_registration(email , token):
    subject = 'Pharma Pill : Activation Code'
    domain = settings.VBcode
    message = f'Welcome to Pharma Pill !! \n Hi {email}, \n Please confirm your email by clicking on the following link.\n \n Confirmation Link: {domain}/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from , recipient_list, fail_silently = True )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('register')
    else:
        return render(request,'activation_failed.html')

 
@login_required(login_url='lgIn')
@login_required
def logOut(request): 
    request.session.clear()
    logout(request)
    return redirect('lgIn') 
 

def forgotPass(request):

    if request.method == 'POST': 
        input_email = request.POST['forgot-email']
        input_password = request.POST['forgot-password']
        input_confirmPassword = request.POST['Conf-forgot-password']

        user = User.objects.filter(username = input_email , email = input_email).first()

    
        if input_password != input_confirmPassword:
            messages.error(request,"Password Didn't Match")
            return redirect('forgotPass')
        elif user is None:
            messages.error(request, "Email Didn't Match")
            return redirect('forgotPass')
        elif (len(input_password) <= 5):
            messages.error(request, "Password must be Six Character Long")
            return redirect('forgotPass')
        else:
            try:
                user_obj = User.objects.get(username = input_email, email = input_email)
                profile_obj = db_Profile.objects.filter(char_email = input_email).first()
                
                myuser = db_Profile.objects.get(char_email = input_email)
                
                if user_obj is None:
                    messages.error(request, 'User not found.')
                else:
                    profile_obj.is_verified = False
                    auth_token = profile_obj.auth_token
                    user_obj.set_password(input_password)
                    myuser.is_verified = False

                    profile_obj.save()
                    user_obj.save()
                    myuser.save()
                    messages.success(request, 'Email Successfully Reset Password, \n We have sent an email to you , \"Please check your mail to Verify Again\"')
                    send_mail_after_registration(input_email , auth_token)
                    return redirect('lgIn')
                        
            except Exception as e:
                print(e)
    return render(request , 'forgotPass.html')
    
# -------------------------------------- ----------------------- reset Password Start ---------------------- //

def changePassword(request):  
    template = loader.get_template('changePassword.html')  
    if request.method == "POST":  
        input_email = request.POST['reset-email']
        input_Oldpassword = request.POST['reset-password']
        input_NewPassword = request.POST['reset-newPassword']
        input_ConfirmPassword = request.POST['Conf-reset-password']

        user_obj = User.objects.filter(username = input_email).first()
        user = authenticate(username = input_email , password = input_Oldpassword)
 
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('setting')
        elif user is None:
            messages.error(request, 'Invalid password.')
            return redirect('setting')
        elif (len(input_NewPassword) <= 5):
            messages.error(request, "New Password must be Six Character Long")
            return redirect('setting')
        elif input_NewPassword != input_ConfirmPassword:
            messages.error(request, "Password didn't Match.")
            return redirect('setting')
        else:
            try:
                user_obj.set_password(input_NewPassword)
                user_obj.save()

                messages.success(request, 'Password Successfully Save Changed.')
                logOut(request, input_email)
                return redirect('lgIn') 

            except Exception as e:
                print(e)
    context = {  }
    return HttpResponse(template.render(context, request))

