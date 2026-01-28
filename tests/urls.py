from django.urls import path
from . import views

urlpatterns = [
    path('create-test/', views.create_test, name='create_test'),
    path('add-questions/<int:test_id>/', views.add_questions, name='add_questions'),
    path('my-tests/', views.my_tests, name='my_tests'),
    path('student/tests/', views.student_tests, name='student_tests'),
    path('student/tests/<int:test_id>/', views.attempt_test, name='attempt_test'),
    path('student/results/', views.student_results, name = 'student_results'),
    path('publish/<int:test_id>', views.publish_test, name = 'publish_test'),
    path('unpublish/<int:test_id>', views.unpublish_test, name = 'unpublish_test'),
    path('delete-test/<int:test_id>', views.delete_test, name = 'delete_test'),
]
