from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .forms import TestForm, QuestionForm
from .models import Test, Question
from users.models import Teacher
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Test, Submission, Answer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'teacher':
            return render(request, 'tests/403.html')
        return view_func(request, *args, **kwargs)
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            return render(request, 'teacher/403.html')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@teacher_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.teacher = request.user.teacher  # link test to logged-in teacher
            test.save()
            return redirect('add_questions', test_id=test.id)
    else:
        form = TestForm()
    return render(request, 'teacher/create_test.html', {'form': form})

@login_required
@teacher_required
def add_questions(request, test_id):
    test = Test.objects.get(id=test_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            form = QuestionForm()  # reset form for next question
    else:
        form = QuestionForm()

    questions = test.questions.all()  # existing questions
    return render(request, 'teacher/add_questions.html', {'form': form, 'test': test, 'questions': questions})

@login_required
@teacher_required
def publish_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user.teacher)
    if test.is_visible == False:
        test.is_visible = True
        test.save()

    return redirect('my_tests')

@login_required
@teacher_required
def unpublish_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user.teacher)
    if test.is_visible == True:
        test.is_visible = False
        test.save()

    return redirect('my_tests')
        
@login_required
@teacher_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id, teacher=request.user.teacher)
    if test:
        test.delete()

    return redirect('my_tests')

@login_required
@teacher_required
def my_tests(request):
    tests = Test.objects.filter(teacher=request.user.teacher).order_by('start_time')
    return render(request, 'teacher/my_tests.html', {'tests': tests, 'current_time' : timezone.now()})

@login_required
@student_required
def student_tests(request):
    now = timezone.now()

    available_tests = Test.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        is_visible = True
    )

    upcoming_tests = Test.objects.filter(
        start_time__gt = now,
        is_visible = True
    ).order_by('start_time')

    return render(request, 'tests/student_tests.html', {
        'available_tests': available_tests,
        'upcoming_tests': upcoming_tests
    })

@login_required
@student_required
def attempt_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if not test.has_started():
        return HttpResponse("Test has not started yet")

    if test.has_ended():
        return HttpResponse("Test has ended")

    if Submission.objects.filter(student=request.user.student, test=test).exists():
        return render(request, 'tests/already_attempted.html', {'test': test})

    if request.method == 'POST':
        
        if timezone.now() > test.end_time:
            return HttpResponse("Submission time is over")
        
        submission = Submission.objects.create(
            student=request.user.student,
            test=test
        )

        for question in test.questions.all():
            selected = request.POST.get(f'question_{question.id}')
            Answer.objects.create(
                submission=submission,
                question=question,
                selected_option=selected
            )
        
        submission.evaluate()

        return redirect('student_tests')

    return render(request, 'tests/attempt_test.html', {'test': test})

@login_required
@student_required
def student_results(request):
    submission = Submission.objects.filter(
        student = request.user.student,
        is_evaluated = True
    )
    return render(request, 'tests/student_results.html', {
        'submissions' : submission
    })