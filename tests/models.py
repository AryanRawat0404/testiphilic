from django.db import models
from users.models import Teacher
from users.models import Student
from django.utils import timezone

class Test(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='tests'
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_marks = models.IntegerField()
    is_visible = models.BooleanField(default=False)

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def has_started(self):
        return timezone.now() >= self.start_time

    def has_ended(self):
        return timezone.now() > self.end_time

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_option = models.CharField(
        max_length=1,
        choices=(
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        )
    )

    marks = models.IntegerField()

    def __str__(self):
        return f"Q: {self.question_text[:40]}"

class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    is_evaluated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'test')

    def evaluate(self):
        total = 0

        for answer in self.answers.all():
            if answer.selected_option == answer.question.correct_option:
                total += answer.question.marks

        self.score = total
        self.is_evaluated = True
        self.save()


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.question.id} - {self.selected_option}"