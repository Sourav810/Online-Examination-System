from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("teacher-home/",views.teacher_home),
    path("teacher-signup/",views.teacher_signup_view),
    path("teacher-login/",views.teacher_login),
    # path("teacher-save/",views.savecandidate),
    path('teacher-dashboard/',views.teacher_dashboard_view),
    path('teacher-exam/', views.teacher_exam_view),
    path('teacher-question/', views.teacher_question_view),
    path('logout/',views.tealogout),
    path('teacher-add-exam/', views.teacher_add_exam_view),
    path('teacher-view-exam/', views.teacher_view_exam_view),
    path('delete-exam/<int:pk>', views.delete_exam_view),
    
    path('teacher-add-question/<int:no>/<int:pk>', views.teacher_add_question_view),
    path('teacher-add-question-no/',views.teacher_add_queno),
    path('teacher-view-question/', views.teacher_view_question_view),
    path('remove-question/<int:pk>', views.remove_question_view),
    path('see-question/<int:pk>', views.see_question_view),

    path('teacher-student/', views.teacher_student_view),
    path('teacher-view-student/', views.teacher_view_student_view),
    path('teacher-view-student-marks/', views.teacher_view_student_marks_view),
    path('teacher-view-marks/<int:pk>', views.teacher_view_marks_view),
    path('teacher-check-marks/<int:pk>', views.teacher_check_marks_view),
    path('update-student/<int:pk>', views.update_student_view),
    path('delete-student/<int:pk>', views.delete_student_view),

    path('activate-exam/<int:pk>',views.activate),

    path('check-result/',views.check_result),
    path('teacher-approve-results/',views.teacher_approve_result),
    path('approve-results/<int:pk>',views.approve_result),
    path('ok-student-result/<int:pk>/<int:dk>',views.ok_student_result),
    path('cheat-student-result/<int:pk>/<int:dk>',views.cheat_student_result),
    path('delete-student-result/<int:pk>/<int:dk>',views.delete_student_result),

    path('set-key/',views.set_exam_key),
    path('set-duration/<int:pk>/',views.set_duration),
]