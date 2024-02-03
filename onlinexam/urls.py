from django.urls import path,include
from django.contrib import admin
from exam import views
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
   
    path('admin/', admin.site.urls),
   # path('pariksha/exam/',include('exam.urls')),
    path('pariksha/student/',include('student.urls')),
    path('pariksha/teacher/',include('teacher.urls')),
    path('pariksha/contactus/',views.contact),
    path('pariksha/contact-success/',views.contactsuccess),
    path('pariksha/',views.home_page),
    path('pariksha/admin-login/',views.adminlogin),
    path('pariksha/admin-dashboard/', views.admin_dashboard_view),
    path('pariksha/admin-logout/',views.adminlogout),
    path('pariksha/admin-query',views.adminquery),
    path('pariksha/delete-query/<int:pk>',views.delete_query),

    path('pariksha/admin-teacher', views.admin_teacher_view),
    path('pariksha/admin-view-teacher', views.admin_view_teacher_view),
    path('pariksha/update-teacher/<int:pk>', views.update_teacher_view),
    path('pariksha/delete-teacher/<int:pk>', views.delete_teacher_view),
    path('pariksha/admin-view-pending-teacher', views.admin_view_pending_teacher_view),
    path('pariksha/approve-teacher/<int:pk>', views.approve_teacher_view),
    path('pariksha/reject-teacher/<int:pk>', views.reject_teacher_view),

    path('pariksha/admin-student', views.admin_student_view),
    path('pariksha/admin-view-student', views.admin_view_student_view),
    path('pariksha/admin-view-student-marks', views.admin_view_student_marks_view),
    path('pariksha/admin-view-marks/<int:pk>', views.admin_view_marks_view),
    path('pariksha/admin-check-marks/<int:pk>', views.admin_check_marks_view),
    path('pariksha/update-student/<int:pk>', views.update_student_view),
    path('pariksha/delete-student/<int:pk>', views.delete_student_view),

    path('pariksha/admin-course', views.admin_course_view),
    path('pariksha/admin-add-course', views.admin_add_course_view),
    path('pariksha/admin-view-course', views.admin_view_course_view),
    path('pariksha/delete-course/<int:pk>', views.delete_course_view),

    path('pariksha/admin-question', views.admin_question_view),
    path('pariksha/admin-add-question-no',views.admin_add_queno),
    path('pariksha/admin-add-question/<int:no>/<int:pk>', views.admin_add_question_view),
    path('pariksha/admin-view-question', views.admin_view_question_view),
    path('pariksha/view-question/<int:pk>', views.view_question_view),
    path('pariksha/delete-question/<int:pk>', views.delete_question_view),

    path('pariksha/set-duration/<int:pk>',views.set_duration),

]
