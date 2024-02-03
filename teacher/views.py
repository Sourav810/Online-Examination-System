from django.shortcuts import render,redirect
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM



from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.models import User
from teacher.models import Teacher
from exam import models as QMODEL


#for showing signup/login button for teacher

def teacher_signup_view(request):
    userForm=forms.TeacherUserForm()
    teacherForm=forms.TeacherForm()
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=forms.TeacherUserForm(request.POST)
        teacherForm=forms.TeacherForm(request.POST,request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
        return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-login')
    return render(request,'teacher/teachersignup.html',context=mydict)
 


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()



# Create your views here.

def teacher_home(request):
    return render(request,'teacher/teacher_home.html')



def tealogout(request):
    std=Teacher.objects.get(user=request.user)
    std.active=0
    std.save()
    request.session['activate']=0
    logout(request)
    return HttpResponseRedirect('http://localhost:8000/pariksha/')

def teacher_login(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
       
        if user:
           abc=User.objects.get(username=username)
           existance=Teacher.objects.filter(user=abc).exists()
           
        if user and existance :
            stat=Teacher.objects.get(user=abc)
            if 'activate'in request.session and request.session['activate']==1 :
                data['error'] = "User is already logged-in, log-out first then log-in"
                return render(request, 'teacher/teacherlogin.html', data)

            if stat.status==False:
                data['error'] = "You are not approved yet, please wait till admin approves you"
                return render(request, 'teacher/teacherlogin.html', data)

            if stat.active==1 :
               data['error'] = "You have already logged-in on other device "
               return render(request, 'teacher/teacherlogin.html', data)
            
            login(request, user)
            stat.active=1
            stat.save()
            request.session['username'] = username
            request.session['activate']=1
            return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-dashboard')
        else:
            data['error'] = "Username or Password is incorrect"
            return render(request, 'teacher/teacherlogin.html', data)
    else:
        return render(request, 'teacher/teacherlogin.html', data)


# def savecandidate(request):
#     if request.method == "POST":
#         data = request.POST
        
#         candid=Teacher()
        
#         candid.profile_pic=data.get('profile_pic')
#         candid.address=data['Add']
#         candid.mobile=data['Cno']
#         candid.status=False
#         b=User.objects.create_user(username=data['Username'],password=data.get('Password'),first_name=data.get('Fname'),last_name=data.get('Lname'))
#         candid.user=b
       
#         candid.save()
#         b.save()
   
#     return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-login/')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacher =Teacher.objects.get(user_id=request.user.id)
    dict={
    
    'total_course':QMODEL.Course.objects.filter(course_teacher=teacher).count(),
    'total_question':QMODEL.Question.objects.filter(course__course_teacher=teacher).count(),
    'total_student':SMODEL.Student.objects.all().count()
    }
    return render(request,'teacher/teacher_dashboard.html',dict)

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request,'teacher/teacher_exam.html')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_question_view(request):
    return render(request,'teacher/teacher_question.html')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
   
    if request.method=='POST':
        data = request.POST
        
        course=QMODEL.Course()
        
        course.course_name=data.get('course_name')
        course.question_number=data.get('question_number')
        course.total_marks=data.get('total_marks')
        course.pass_marks=data.get('pass_marks')
        teacher =Teacher.objects.get(user_id=request.user.id)
        course.course_teacher=teacher
        course.hou=data.get('hour')
        course.minu=data.get('minute')
        course.sec=data.get('second')
        course.save()
        return HttpResponseRedirect('/pariksha/teacher/teacher-view-exam')
    else :
        return render(request,'teacher/teacher_add_exam.html')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    teacher =Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.filter(course_teacher=teacher)
    return render(request,'teacher/teacher_view_exam.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def delete_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/pariksha/teacher/teacher-view-exam')

#  working but css problem-----
@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_add_queno(request):
    teacher =Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.filter(course_teacher=teacher)
    if request.method=="POST":
        qno=request.POST.get('qno')
        course_id=request.POST.get('courseID')
        return HttpResponseRedirect("/pariksha/teacher/teacher-add-question/"+(str)(qno)+"/"+(str)(course_id))
    return render(request,'teacher/teacher_add_question_no.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_add_question_view(request,no,pk):
    courses=QMODEL.Course.objects.all()
    course=QMODEL.Course.objects.get(id=pk)
    teacher =Teacher.objects.all()
    li=[]
    for i in range(1,no+1):
            li.append(i)
    if request.method=='POST':
    
        data = request.POST
        for i in range(1,no+1):
            que=QMODEL.Question()
            que.course_id=pk
            que.marks=data.get('marks'+(str)(i))
            que.question=data.get('question'+(str)(i))
            que.option1=data.get('option1'+(str)(i))
            que.option2=data.get('option2'+(str)(i))
            que.option3=data.get('option3'+(str)(i))
            que.option4=data.get('option4'+(str)(i))
            que.answer=data.get('answer'+(str)(i))
            que.save()
        return HttpResponseRedirect('/pariksha/teacher/teacher-view-question')
    return render(request,'teacher/teacher_add_question.html',{'courses':courses,'course':course,'teachers':teacher,'list':li})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    teacher =Teacher.objects.get(user_id=request.user.id)
    courses= QMODEL.Course.objects.filter(course_teacher=teacher)
    return render(request,'teacher/teacher_view_question.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def see_question_view(request,pk):
    questions=QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request,'teacher/see_question.html',{'questions':questions})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def remove_question_view(request,pk):
    question=QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/pariksha/teacher/teacher-view-question/')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'teacher/teacher_student.html',context=dict)

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'teacher/teacher_view_student.html',{'students':students})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'teacher/teacher_view_student_marks.html',{'students':students})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_view_marks_view(request,pk):
    teacher =Teacher.objects.get(user_id=request.user.id)
    courses= QMODEL.Course.objects.filter(course_teacher=teacher)
    response =  render(request,'teacher/teacher_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_check_marks_view(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'teacher/teacher_check_marks.html',{'results':results})

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
   
    mydict={'user':user,'student':student}
    if request.method=='POST':
        data=request.POST
        user.username=data.get('username')
        user.set_password(data.get('password'))
        user.first_name=data.get('first_name')
        user.last_name=data.get('last_name')
        user.save()
        student.user=user
        student.address=data.get('address')
        student.mobile=data.get('mobile')
        student.save()
        return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-view-student')
           
    return render(request,'teacher/teacher_student.html',context=mydict)

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-view-student')

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def activate(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    stat=course.active
    if(stat==0):
        course.active=1
    else:
        course.active=0
    course.save()
    return HttpResponseRedirect("http://localhost:8000/pariksha/teacher/teacher-view-exam")

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def check_result(request): 
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'teacher/check_result.html',context=dict)

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def set_exam_key(request):
    teacher =Teacher.objects.get(user_id=request.user.id)
    if request.method=='POST':
        teacher.exam_password=request.POST.get('exam_key')
        teacher.save()
        return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-dashboard')
    
    return render(request,'teacher/set_exam_key.html',{'teacher':teacher})
    
@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def set_duration(request,pk):
    course = QMODEL.Course.objects.get(id=pk)
    if request.method=='POST':
        course.hou=request.POST.get('hour')
        course.minu=request.POST.get('minute')
        course.sec=request.POST.get('second')
        course.save()
        return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/teacher-view-exam/')
    return render(request,'teacher/set_duration.html',{"course":course})



@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def teacher_approve_result(request): 
    teacher =Teacher.objects.get(user_id=request.user.id)
    courses = QMODEL.Course.objects.filter(course_teacher=teacher)
    total_student=SMODEL.Student.objects.all().count()
    results=QMODEL.Result.objects.all()
    # appeared_student=QMODEL.Result.objects.all(exam=).count()
    return render(request,'teacher/teacher_approve_result.html',{'courses':courses,'total_student':total_student,'results':results})
    

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def approve_result(request,pk): 
    course = QMODEL.Course.objects.get(id=pk)
    results=QMODEL.Result.objects.filter(exam=course)
    exam_pics=QMODEL.Exam_pic.objects.filter(exam=course)
    return render(request,'teacher/approve_result.html',{'course':course,'results':results,'exam_pics':exam_pics})


@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def ok_student_result(request,pk,dk):
    course = QMODEL.Course.objects.get(id=pk)
    student=SMODEL.Student.objects.get(id=dk)
    result = QMODEL.Result.objects.get(exam=course,student=student)
    result.checked=1
    result.save()
    return HttpResponseRedirect("http://localhost:8000/pariksha/teacher/approve-results/"+(str)(pk))


@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def delete_student_result(request,pk,dk):
    course = QMODEL.Course.objects.get(id=pk)
    student=SMODEL.Student.objects.get(id=dk)
    result = QMODEL.Result.objects.get(exam=course,student=student)
    exam_pic=QMODEL.Exam_pic.objects.get(exam=course,student=student)
    result.delete()
    exam_pic.delete()
    
    return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/approve-results/'+(str)(pk))

@login_required(login_url='http://localhost:8000/pariksha/teacher/teacher-login')
@user_passes_test(is_teacher)
def cheat_student_result(request,pk,dk):
    course = QMODEL.Course.objects.get(id=pk)
    student=SMODEL.Student.objects.get(id=dk)
    result = QMODEL.Result.objects.get(exam=course,student=student)
    result.checked=3
    result.save()
    return HttpResponseRedirect('http://localhost:8000/pariksha/teacher/approve-results/'+(str)(pk))