from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout 
from account.forms import RegistrationForm, AccountAuthenticationForm, AccontUpdateForm
from blog.models import BlogPost


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, "account/register.html", context)

    
def logoutUser(request):
    logout(request)    # use the imported logout
    return redirect('login')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

        # if user exists means is successfully authenticated 

            if user:
                login(request, user)
                return redirect("home")

    else:   #if user is not authenticated redirect to the login page
        form =  AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        form = AccontUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Successfully Updated"

    else:
        form = AccontUpdateForm(
            initial = {
                "email": request.user.email,
                "username":request.user.username,
            }
        )
    context['account_form'] = form

    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts
    return render(request, 'account/account.html', context)


def must_authenticate(request):

    return render(request, 'account/must_authenticate.html', {})