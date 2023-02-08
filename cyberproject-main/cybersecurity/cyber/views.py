import datetime
import os
import random
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from . models import User
from . import sendmail
from .forms import UserForm, MyUserCreationForm, UpdateUserPasswordForm

# Create your views here.

def loginUser(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                user.is_loggedin = True
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        except:
            messages.error(request, 'User does not exist.')
    context = {'page': page}
    return render(request, 'cyber/login_register.html', context)


def registerUser(request):
    page = "Sign Up"
    if request.user.is_authenticated:
        return redirect('home')
    try:
        form = MyUserCreationForm()
        if request.method == 'POST':
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                print("TRUE")
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.is_registered = True
                tok = str(random.randint(111111, 99999999999)) + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':', '').replace(',', '').replace('-', '').replace(' ', '')
                user.token = tok
                user.save()
                # Send email notification
                to = user.email
                subject = 'Account Creation for Cyber Arena'
                regMsg = sendmail.EmailMessages(user.token, user.username)
                emailMsg, alt = regMsg.registerMsg()
                print("Email message: ", emailMsg, "Alt message: ", alt, sep="\n")
               
                sendmail.SendMail(to, subject, emailMsg, alt)
                messages.success(request, f"You account was created successfully. You will receive an message shortly at {user.email} to confirm your email.")
                # end email notification
                return redirect('home')
            else:
                e_str = ""
                err = list(form.errors.values())
                for i in range(len(err)):
                    if err[i - 1][0] == err[i][0]:
                        err[i][0] = err[i - 1][0]
                    e_str = e_str + err[i][0]
                if e_str == '':
                    e_str = 'You cannot submit a form with empty fields.'
                messages.error(request, e_str+"\n")
        context = {'form': form, 'page': page}
        return render(request, 'cyber/login_register.html', context)
    except Exception as e:
        messages.error(request, "Something went wrong during registration.")
        return redirect('register')


def confirmAccount(request, tok):
    user = User.objects.get(token=tok)
    # print("CONFIRM USER QUERY: ", user.query)
    if user.is_active == True:
        messages.error(request, "Your account is already confirmed.")
        return redirect('login')
    elif user.is_active == False and user.is_registered == True:
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been confirmed successfully.")
        return redirect('login')
    else:
        messages.error(request, "Invalid user account")
        return redirect('register')
    


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    context = {}
    return render(request, 'cyber/home.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'cyber/update_user.html', {'form: form'})


@login_required(login_url='login')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'cyber/profile.html', context)


@login_required(login_url='login')
def bookAppointment(request):
    context = {}
    return render(request, 'cyber/appointment.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            user = User.objects.get(email=email)
            if user.is_registered == True:
                # return redirect('changepass', pk=email)
                tok = str(random.randint(111111, 99999999999)) + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).replace(':', '').replace(',', '').replace('-', '').replace(' ', '')
                user.token = tok
                user.save()
                # Send email notification
                to = user.email
                subject = 'Reset password for Cyber Arena'
                resetMsg = sendmail.EmailMessages(tok, None)
                emailMsg, alt = resetMsg.resetPasswordMsg(to)
                sendmail.SendMail(to, subject, emailMsg, alt)
                messages.success(request, f"You will receive an message shortly at {user.email} to reset your password.")
            else:
                messages.error(request, 'Incorrect email address.')
        except Exception as e:
            messages.error(request, 'Incorrect email address.')
    context = {"page":"Forgot password"}
    return render(request, 'cyber/forgotpassword.html', context)


def resetPassword(request, tok):
    user = User.objects.get(token=tok)
    if user:
        email = user.email
        return redirect('changepass', pk=email)
    else:
        messages.error(request, 'Incorrect email address provided.')
        return redirect('forgotpass')

def changePassword(request, pk):
    user = User.objects.get(email=pk)
    form = UpdateUserPasswordForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserPasswordForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            subject = "Successfully password update for Cyber Arena"
            passChgMsg = sendmail.EmailMessages(None, None)
            emailMsg, alt = passChgMsg.passChangedMsg()
            sendmail.SendMail(user.email, subject, emailMsg, alt)
            messages.success(request, 'Password changed successfully.')
            return redirect('login')
    context = {"email": pk, "form":form, "page": "Create your new password"}
    return render(request, 'cyber/changepassword.html', context)