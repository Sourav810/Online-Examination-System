from django.contrib import admin

# Register your models here.
from exam.models import Course, Question,Result,Message,Exam_pic
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Message)
admin.site.register(Exam_pic)