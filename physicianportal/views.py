from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PhysicianRegistrationForm



def physicianregistration(request):
    if request.method == 'POST':
        form = PhysicianRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('physicianlogin')

    else:
        form = PhysicianRegistrationForm()
    return render(request, 'physicianportal/physicianregistration.html', {'form': form})


@login_required
def physicianprofile(request):
    return render(request, 'physicianportal/physicianprofile.html')
