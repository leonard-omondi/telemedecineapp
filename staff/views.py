from django.shortcuts import render, redirect
from django.contrib import messages
from .staff_forms import StaffRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


def staff_registration(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login')
            return redirect('stafflogin')
    else:
        form = StaffRegistrationForm()
    return render(request, 'staff/staffregistration.html', {'staffform': form})


@login_required
def staff_portal(request):
    return render(request, 'staff/staff.html')


@login_required
def staff_profile(request):
    return render(request, 'staff/staffprofile.html')


class StaffLogin(LoginView):
    template_name = 'staff/stafflogin.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url
