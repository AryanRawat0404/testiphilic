from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

# Create your views here.
@login_required
@role_required(['student'])
def student_dashboard(request):
    return render(request, 'dashboard/student.html')

@login_required
@role_required(['teacher'])
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher.html')

@login_required
@role_required(['principal'])
def principal_dashboard(request):
    return render(request, 'dashboard/principal.html')