import cv2
import os
from PIL import Image
from datetime import datetime,timedelta
import random
from exam.models import Question,Result,Course,Exam_pic
from student.models import Student
from onlinexam.settings import STATIC_DIR
from django import template
register=template.Library()



@register.simple_tag(name="VideoCamera")
def VideoCamera(user_id,course_id):
    cam=cv2.VideoCapture(0)
    cv2.namedWindow("Python webcam Screenshot App")
    ran_time=random.randint(3,10)
    while True:
        ret,frame=cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test",frame)
        img_name="opencv_frame_{}_{}_{}.jpg".format(user_id,course_id,ran_time)
        path=os.path.join(STATIC_DIR,'exam_pic')
        img=cv2.imwrite(os.path.join(path,img_name),frame)

        print("screenshot taken", ran_time)
        break

    set_image(user_id,course_id,img_name)
    cam.release()
    cv2.destroyAllWindows()

def set_image(user_id,course_id,img_name):
    
    course=Course.objects.get(id=course_id)
    student=Student.objects.get(user_id=user_id)
   
    result=Exam_pic(exam=course,student=student)
    # result.exam_pic.save(img_name,'/static/exam_pic')
    result.exam_pic="/static/exam_pic/{}".format(img_name)
    result.save()
    print("YES it is working", course.course_name,student.user)