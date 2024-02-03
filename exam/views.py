from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from teacher import models as TMODEL
from student import models as SMODEL
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from . import models

def home_page(request):
    return render(request,'exam/home_page.html')

def contact(request):
    return render(request,'exam/contactus.html')
    

def contactsuccess(request):
    if request.method=="POST":
        mess=models.Message()
        mess.name=request.POST.get('Name')
        name=request.POST.get('Name')
        mess.email=request.POST.get('Email')
        mess.mobile=request.POST.get('Mobile')
        mess.message=request.POST.get('Message')
        mess.save()
    
        return render (request,'exam/contactpage.html',{'name':name})
    return HttpResponseRedirect('/pariksha/contactus')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def adminquery(request):
    queries= models.Message.objects.all()
    return render(request,'exam/admin_viewquery.html',{'queries':queries})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def delete_query(request,pk):
    query=models.Message.objects.get(id=pk)
    query.delete()
    return HttpResponseRedirect('/pariksha/admin-query')

def adminlogout(request):
    request.session['activate']=0
    logout(request)
    return HttpResponseRedirect('/pariksha')

def adminlogin(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            abc=User.objects.get(username=username)
            existance=abc.is_superuser
        if user and existance:
            if 'activate'in request.session and request.session['activate']==1 :
                data['error'] = "User is already logged-in, log-out first then log-in"
                return render(request, 'exam/admin_login.html', data)
            login(request, user)
            request.session['username'] = username
            request.session['activate']=1
            return HttpResponseRedirect('http://localhost:8000/pariksha/admin-dashboard/')
        else:
            data['error'] = "Username or Password is incorrect"
            return render(request, 'exam/admin_login.html', data)
    else:
        return render(request, 'exam/admin_login.html', data)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_dashboard_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    }
    return render(request,'exam/admin_dashboard.html',dict)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
   
    }
    return render(request,'exam/admin_teacher.html',dict)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def update_teacher_view(request,pk):

        teacher=TMODEL.Teacher.objects.get(id=pk)
        user=TMODEL.User.objects.get(id=teacher.user_id)
        mydict={'user':user,'teacher':teacher}
        if request.method=='POST':
                data=request.POST
                user.username=data.get('username')
                user.set_password(data.get('password'))
                user.first_name=data.get('first_name')
                user.last_name=data.get('last_name')
                user.save()
                teacher.user=user
                teacher.address=data.get('address')
                teacher.mobile=data.get('mobile')
                teacher.profile_pic=request.FILES.get('profile_pic')
                teacher.save()
                return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-teacher')
        return render(request,'exam/update_teacher.html',context=mydict)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/pariksha/admin-view-teacher')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_pending_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def approve_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    
    teacher.status=True
    teacher.save()
    return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-pending-teacher')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-pending-teacher')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
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
        student.profile_pic=request.FILES.get('profile_pic')
        student.save()
        return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-student')
           
    return render(request,'exam/update_student.html',context=mydict)

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-student')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_add_course_view(request):
    teacher = TMODEL.Teacher.objects.all()
    if request.method=='POST':
        data=request.POST
        course=models.Course()
        course.course_name=data.get('course_name')
        course.question_number=data.get('question_number')
        course.total_marks=data.get('total_marks')
        course.pass_marks=data.get('pass_marks')
        tea=data.get('teacher')
        course.course_teacher=TMODEL.Teacher.objects.get(id=tea)
        course.hou=request.POST.get('hour')
        course.minu=request.POST.get('minute')
        course.sec=request.POST.get('second')
        course.save()
        return HttpResponseRedirect('/pariksha/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'teachers':teacher})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})
 
@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/pariksha/admin-view-course')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')

#  working but css problem-----
@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_add_queno(request):
    courses=models.Course.objects.all()
    if request.method=="POST":
        qno=request.POST.get('qno')
        course_id=request.POST.get('courseID')
        return HttpResponseRedirect("/pariksha/admin-add-question/"+(str)(qno)+"/"+(str)(course_id))
    return render(request,'exam/admin_add_question_no.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_add_question_view(request,no,pk):
    courses=models.Course.objects.all()
    course=models.Course.objects.get(id=pk)
    teacher = TMODEL.Teacher.objects.all()
    li=[]
    for i in range(1,no+1):
        li.append(i)
    if request.method=='POST':
     
        data = request.POST
        for i in range(1,no+1):
            que=models.Question()
            que.course_id=pk
            que.marks=data.get('marks'+(str)(i))
            que.question=data.get('question'+(str)(i))
            que.option1=data.get('option1'+(str)(i))
            que.option2=data.get('option2'+(str)(i))
            que.option3=data.get('option3'+(str)(i))
            que.option4=data.get('option4'+(str)(i))
            que.answer=data.get('answer'+(str)(i))
            que.save()
        return HttpResponseRedirect('/pariksha/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'courses':courses,'course':course,'teachers':teacher,'list':li})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/pariksha/admin-view-question')

@login_required(login_url='http://localhost:8000/pariksha/admin-login')
def set_duration(request,pk):
    course = models.Course.objects.get(id=pk)
    if request.method=='POST':
        course.hou=request.POST.get('hour')
        course.minu=request.POST.get('minute')
        course.sec=request.POST.get('second')
        course.save()
        return HttpResponseRedirect('http://localhost:8000/pariksha/admin-view-course')
    return render(request,'exam/set_duration.html',{"course":course})