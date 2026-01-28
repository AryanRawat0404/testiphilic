from django.contrib import admin
from .models import Test, Question, Submission, Answer

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Answer)
