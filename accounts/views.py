from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            role = user.profile.role

            if role == 'principal':
                return redirect('principal_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

    return render(request, 'accounts/login.html')