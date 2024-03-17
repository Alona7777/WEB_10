from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


# Create your views here.
def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:root')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'users/register.html', context={"form": form})

    return render(request, 'users/register.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
       return redirect(to='quotes:root')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes:root')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:root')

# class RegisterView(View):
#     template_name = 'users/register.html'
#     form_class = RegisterForm

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect(to='quotes:root')
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request):
#         return render(request, self.template_name, {'form': self.form_class})

#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             messages.success(request, f'Hello {username}. Your account successfully created!')
#             return redirect(to='users:login')
#         return render(request, self.template_name, {'form': form})