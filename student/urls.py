from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
path("student-home/",views.student_home),
    path("student-signup/",views.student_signup_view),
    path("student-login/", views.student_login),
    # path("student-save/", views.savecandidate),
    path("student-dashboard/", views.student_dashboard_view),
    path('student-exam/', views.student_exam_view),
    path('student-marks/', views.student_marks_view),
    path('logout/',views.stdlogout),
    path('take-exam/<int:pk>', views.take_exam_view),
    path('start-exam/<int:pk>', views.start_exam_view),
    path('check-marks/<int:pk>', views.check_marks_view),
    path('calculate-marks/<int:pk>', views.calculate_marks_view),
    path('view-result/', views.view_result_view),

    path('take-exam-key/<int:pk>',views.take_exam_key),

    path('pie_chart_view/<int:pk>',views.pie_chart_view),
    path('progress_view/',views.progress_view),
    path('show_result/<int:pk>',views.show_result),
]