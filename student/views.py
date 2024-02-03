from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from student.models import Student

from student import models
from teacher.models import Teacher
import datetime



def student_home(request):
    return render(request,'student/student_home.html')


def stdlogout(request):
    std=Student.objects.get(user=request.user)
    std.active=0
    std.save()
    request.session['activate']=0
    del request.session['activate']
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/pariksha/')

def student_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
           abc=User.objects.get(username=username)
           existance=Student.objects.filter(user=abc).exists()
           
        if user and existance :
            std=Student.objects.get(user=abc)
            if 'activate'in request.session and request.session['activate']==1 :
                data['error'] = "User is already logged-in, log-out first then log-in"
                return render(request, 'student/studentlogin.html', data)

            if std.active==1 :
               data['error'] = "You have already logged-in on other device "
               return render(request, 'student/studentlogin.html', data)

            login(request, user)
            std.active=1
            std.save()
            request.session['username'] = username
            request.session['activate']=1
            return HttpResponseRedirect('http://localhost:8000/pariksha/student/student-dashboard')
        else:
            data['error'] = "Username or Password is incorrect"
            return render(request, 'student/studentlogin.html', data)
    else:
        return render(request, 'student/studentlogin.html', data)


# def savecandidate(request):
#     if request.method == "POST":
#         data = request.POST
        
#         candid=Student()
       
#         candid.profile_pic=data.get('profile_pic')
#         candid.address=data['Add']
#         candid.mobile=data['Cno']
        
#         b=User.objects.create_user(username=data.get('Username'),password=data.get('Password'),first_name=data.get('Fname'),last_name=data['Lname'])
#         candid.user=b
       
#         candid.save()
#         b.save()
   
#     return HttpResponseRedirect('http://localhost:8000/pariksha/student/student-login/')

#for showing signup/login button for student


def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('http://localhost:8000/pariksha/student/student-login/')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',dict)

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    student =models.Student.objects.get(user_id=request.user.id)
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'student':student,'course_id':pk})
   # response.set_cookie('course_id',course.id)
    return response

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student =models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results,'course':course})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def calculate_marks_view(request,pk):
    if request.method=='POST':
       # if request.COOKIES.get('course_id') is not None:
        course_id = pk
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in questions:
            #if request.POST.get((str)(i.id)) != None:
            selected_ans = request.POST.get((str)(i.id))
            actual_answer = i.answer
            if selected_ans == actual_answer:
                total_marks = total_marks + i.marks
        
        student = models.Student.objects.get(user_id=request.user.id)
       
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.date=datetime.datetime.now()
        result.save()

        return HttpResponseRedirect('/pariksha/student/student-dashboard/')
    else:
        return HttpResponseRedirect('/pariksha/student/student-login/')

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def take_exam_key(request,pk):
    data = {}
    course=QMODEL.Course.objects.get(id=pk)
    student =models.Student.objects.get(user_id=request.user.id)
    result= QMODEL.Result.objects.all().filter(exam=course).filter(student=student).count()
    
    data['course']=course
    data['student']=student
    data['result']=result
    if request.method=='POST':
        passcode=request.POST.get('exam_key')
        teacher=course.course_teacher
        
        if teacher.exam_password==passcode and result<1:
            return HttpResponseRedirect('http://localhost:8000/pariksha/student/take-exam/'+(str)(pk))
        
        elif result>=1:
            data['error'] = "!!!  You have already attempted this exam. Please contact to your teacher.  !!! "
            return render(request,'student/take_exam_key.html',data)
        
        else :
            data['error'] = "Wrong Exam Key. Provide correct one to appear in the exam."
            return render(request,'student/take_exam_key.html',data)
        
    return render(request,'student/take_exam_key.html',data)

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def pie_chart_view(request,pk):
    result=QMODEL.Result.objects.get(id=pk)
    course=result.exam
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_que=questions.count()
    return render(request,'student/pie_chart.html',{'course':course,'question':questions,'result':result,'total_que':total_que})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def progress_view(request):
    student =models.Student.objects.get(user_id=request.user.id)
    results=QMODEL.Result.objects.filter(student=student)
    return render(request,'student/progress_view.html',{'student':student,'results':results})

@login_required(login_url='http://localhost:8000/pariksha/student/student-login')
@user_passes_test(is_student)
def show_result(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student=Student.objects.get(user_id=request.user.id)
    result=QMODEL.Result.objects.get(exam=course,student=student)
    num=(9999*student.id)+9856+(9999*course.id)+8745+(9999*result.id)
    return render(request,'student/result.html',{'course':course,'student':student,'result':result,'no':num})

 