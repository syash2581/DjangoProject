from django.shortcuts import render
from django.contrib import auth
from django.template.context_processors import csrf
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from SSV.models import  Student, Subject, Voted, Limit, Admin, Result
from django.db.models import Count
from datetime import date
import datetime
from django.contrib import messages
from django.core.mail import send_mail
import random
from PROJECT.settings import EMAIL_HOST_USER

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


#the decorator
def myuser_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'student_id' not in request.session.keys():
                        return HttpResponseRedirect("/SSV/login")
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


#the decorator
def myadmin_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'admin_id' not in request.session.keys():
                        return HttpResponseRedirect("/SSV/admin_login")
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


# Create your views here.


def get_month():
    current_time = datetime.datetime.now()
    return str(current_time.month)

def get_day():
    current_time = datetime.datetime.now()
    return str(current_time.day)

def get_year():
    current_time = datetime.datetime.now()
    return str(current_time.year)

# def login_required(request):
#     if request.session.has_key('student_id'):
#         return True
#     else:
#         return HttpResponseRedirect('login')

@myuser_login_required
def edit_profile(request):

    if request.method == 'POST':

        student_id = request.session['student_id']
        student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
        student_dict = {'student':student_name}

        student_email = request.POST.get('student_email')
        student_name = request.POST.get('student_name')

        if student_email != '' and student_name != '':
            Student.objects.filter(student_id__exact=student_id).update(student_email=student_email, student_name=student_name)
        elif student_email != '':
            Student.objects.filter(student_id__exact=student_id).update(student_email=student_email)
        elif student_name != '':
            Student.objects.filter(student_id__exact=student_id).update(student_name=student_name)

        return HttpResponseRedirect('profile')

    print("Inside edit profile")
    return render(request, 'edit_profile.html', context=None)


@myuser_login_required
def index(request):

    day = get_day()
    month = get_month()

    print(day)
    print(month)
     
    student_id = request.session['student_id'] 
    
    voted_list = Student.objects.values('student_voted').filter(student_id__exact=student_id).get()        
    print(voted_list['student_voted'])

    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    semester_dict = Student.objects.values('student_semester').filter(student_id__exact=student_id).get()
    semester = int(semester_dict['student_semester'])

    limit_dict = Limit.objects.values('limit_subject').filter(limit_semester__exact=semester).get()
    limit = limit_dict['limit_subject']

    print("limit:",limit)    

    subject_list = Subject.objects.order_by('subject_semester').filter(subject_semester__exact=semester)

    choices = request.POST.getlist('subject_choice')
    print(choices)

    limit_subject = len(choices)
    print(limit_subject)

    dictionary = {}

    if semester%2==0:
        semester_ = 0
        print("in 4")
        if month == '4' and day == '26':
            result_dict = Voted.objects.values('subject_id').order_by().annotate(Count('subject_id')).filter(semester=semester)
            print(result_dict)
            count = {}

            for result in result_dict:
                count[result['subject_id']] = result['subject_id__count']
                print(count)
                print(result)

            count_order = sorted(count.items(), reverse=True, key=lambda x: x[1])
            count_order = dict(count_order)
            print("c: ",count_order)
            i=0

            print("---------------------------------------")
            dictionary = {}

            for key,val in count_order.items():
        
                if i < limit:
                    
                    print('value:', val)
                    subject_print = Subject.objects.values('subject_name').filter(subject_id__exact=key).get()
                    
                    rd = Result.objects.create(result_subject=subject_print['subject_name'], result_semester = semester, result_year = get_year(), result_votes=int(val))
                    rd.save()

                    # j = 1
                    # for row in Result.objects.all().reverse():
                    #     if Result.objects.filter(result_semester=i).count() > 1:
                    #         row.delete()
                    #     j = j+1

                    

                    dictionary[subject_print['subject_name']] = val
                    print(val)
                    i = i+1
                else:
                    break
    
            print(dictionary)

    else:
        semester_ = 1
        print("in 5")
        if month == '4' and day == '26':
            result_dict = Voted.objects.values('subject_id').order_by().filter(semester=semester).annotate(Count('subject_id'))
            print(result_dict)
            count = {}

            for result in result_dict:
                count[result['subject_id']] = result['subject_id__count']
                print(count)
                print(result)

            count_order = sorted(count.items(), reverse=True, key=lambda x: x[1])
            count_order = dict(count_order)
            print("c: ",count_order)
            i=0

            print("---------------------------------------")
            dictionary = {}

            for key,val in count_order.items():
        
                if i < limit:
                    print("value:",val)
                    print("key:",key)
                    subject_print = Subject.objects.values('subject_name').filter(subject_id__exact=key).get()
                    
                    rd = Result.objects.create(result_subject=subject_print['subject_name'], result_semester = semester, result_year = get_year(), result_votes=int(val))
                    rd.save()

                    # j = 1
                    # for row in Result.objects.all().reverse():
                    #     if Result.objects.filter(result_semester=i).count() > 1:
                    #         row.delete()
                    #     j = j+1                    

                    dictionary[subject_print['subject_name']] = val
                    print(val)
                    i = i+1
                else:
                    break
    
            print(dictionary)

    for row in Result.objects.all().filter(result_semester=semester).filter(result_year=int(get_year())):                
        if Result.objects.filter(result_semester=semester).filter(result_year=int(get_year())).count() > int(limit):
            print("semester: ", semester)
            print(row)
            row.delete()

    main_result = Result.objects.values('result_subject', 'result_votes').filter(result_semester=semester).filter(result_year=int(get_year()))

    subject_dict = {'subject':subject_list, 'voted_list':voted_list, 'student':student_name, 'limit':limit, 'semester':semester_, 'subject_print':dictionary, 'day':day, 'month':month, 'results':main_result}
    print(subject_dict)


    if request.method == 'POST':                

        if limit == limit_subject:

            print("in limit")

            student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
            student_dict = {'student':student_name}

            for choice in choices:
                print(choice)

                subject_list = Subject.objects.values('subject_id').filter(subject_name__exact=choice).get()
                subject_id = subject_list['subject_id']

                student = Student.objects.get(student_id=student_id)
                subject = Subject.objects.get(subject_id=subject_id)

                vote = Voted.objects.create(subject_id=subject, student_id=student, semester=semester)
                vote.save()

                Student.objects.filter(student_id__exact=student_id).update(student_voted=True)

            print(subject_id)

            return HttpResponseRedirect('thankyou')

        else:
            messages.info(request, 'You have voted less or more subjects. Only vote subject under limit.')

    return render(request, "index.html", context=subject_dict)

@myuser_login_required
def user_logout(request):

    del request.session['student_id']
    print('logout here!!!!')
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect('/SSV/login')

@myadmin_login_required
def admin_logout(request):

    del request.session['admin_id']
    print('logout here!!!!')
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect('/SSV/admin_login')

def user_login(request):

    if request.method == 'POST':
        # c = {}
        # c.update(csrf(request))

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        print(username)
        print(password)

        
        # print(user.student_approve)
        # print(user)

        #user = auth.authenticate(username=username, password=password)
        #auth.login(request, user)

        if Student.objects.filter(student_name__exact=username, student_password__exact=password).count() == 1:    

            user = Student.objects.filter(student_name__exact=username, student_password__exact=password).get()

            if user.student_approve:

                #login(request,user)               
                request.session['student_id'] = str(user.student_id)
                return HttpResponseRedirect(reverse('index'))

            else:
                messages.info(request, 'Your account is not approved yet!!')                

        else:
            messages.info(request, 'Invalid login details!!')            
    else:
        return render(request, 'login.html', context=None)

    return render(request, 'login.html', context=None)    


def forgot_password(request):

    if request.method == 'POST':
        if Student.objects.filter(student_college_id=request.POST.get('college_id')).count() == 0:
            messages.error(request, 'Invalid college id')
        else:
            email = Student.objects.values('student_email').filter(student_college_id=request.POST.get('college_id')).get()
            print(email)
            code_num = random.randrange(100000, 999999)
            print(code_num)
            request.session['code'] = str(code_num) 
            request.session['college_id'] = request.POST.get('college_id')       

            subject = 'Recovery code'
            message = str(code_num)
            recepient = email['student_email']
            send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)

            return HttpResponseRedirect('code')

    return render(request, 'forgot-password.html', context=None)

def code(request):

    if request.method == 'POST':
        code = request.POST.get('code')

        if code == request.session['code']:
            return HttpResponseRedirect('change')
        else:
            messages.error(request, 'Invalid code!!')

    return render(request, 'code.html', context=None)

def change(request):

    if request.method == 'POST':
        if request.POST.get('new_password') != request.POST.get('re_new_password'):            
            messages.error(request, 'Both password field must be same!!')
        else:
            Student.objects.filter(student_college_id__exact=request.session['college_id']).update(student_password=str(request.POST.get('new_password')))
            del request.session['code']
            del request.session['college_id']
            messages.success(request, 'New password has been set')
            return HttpResponseRedirect('login')

    return render(request, 'change.html', context=None)

def about_us(request):

    student_id = request.session['student_id']
    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    student_dict = {'student':student_name}

    return render(request, 'about-us.html', context=student_dict)


@myuser_login_required
def statistics(request):

    student_id = request.session['student_id']
    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    semester_dict = Student.objects.values('student_semester').filter(student_id__exact=student_id).get()
    semester = int(semester_dict['student_semester'])
    limit_dict = Limit.objects.values('limit_subject').filter(limit_semester__exact=semester).get()
    limit = limit_dict['limit_subject']

    # for row in Result.objects.all().reverse():        
    #     if Result.objects.filter(result_semester=semester).filter(result_year=int(get_year())).count() > int(limit):
    #         row.delete()

    year = int(get_year()) - 1
    print(year)
    results = Result.objects.values('result_subject', 'result_semester', 'result_year').filter(result_year=str(year)).filter(result_semester=int(semester))
    print(results)
    student_dict = {'student':student_name, 'results':results}

    return render(request, 'statistics.html', context=student_dict)

@myuser_login_required
def contact_us(request):
    student_id = request.session['student_id']
    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    student_dict = {'student':student_name}
    return render(request, 'contact-us.html', context=student_dict)

@myuser_login_required
def thankyou(request):

    student_id = request.session['student_id']
    semester_dict = Student.objects.values('student_semester').filter(student_id__exact=student_id).get()
    semester = semester_dict['student_semester']

    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    student_dict = {'student':student_name}

    return render(request, "thankyou.html", context=student_dict)


def registration(request):

    if request.method == 'POST':
        c = {}
        c.update(csrf(request))

        student_name = request.POST.get('student_name', '')
        student_email = request.POST.get('student_email', '')
        student_password = request.POST.get('student_password', '')
        student_semester = request.POST.get('student_semester', '')
        student_college_id = request.POST.get('student_college_id', '').lower()

        print(student_name)
        print(student_email)
        print(student_password)
        print(student_semester)

        register = Student.objects.create(student_name=student_name, student_email=student_email, student_password=student_password, student_semester=student_semester, student_college_id=student_college_id)
        register.save()

        return HttpResponseRedirect('login')

    return render(request, 'registration.html', context=None)


@myuser_login_required
def profile(request):
    print("Inside profile")
    profile_list = Student.objects.values('student_name', 'student_email').filter(student_id=request.session['student_id']).get()

    student_id = request.session['student_id']
    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()    

    profile_dict = {'profile_info':profile_list, 'student':student_name}

    print(profile_dict)

    return render(request, 'profile.html', context=profile_dict)


@myuser_login_required
def change_password(request):

    student_id = request.session['student_id']
    student_name = Student.objects.values('student_name').filter(student_id__exact=student_id).get()
    student_dict = {'student':student_name}


    if request.method == 'POST':

        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')
        current_password = request.POST.get('current_password')
        current_list = student_name = Student.objects.values('student_password').filter(student_id__exact=student_id).get()

        if current_password == current_list['student_password'] :

            if new_password == re_new_password:            
                Student.objects.filter(student_id__exact=student_id).update(student_password=new_password)
                #messages.success(request, 'Password has been changed!!')
                return HttpResponseRedirect('profile')
            else:
                messages.error(request, 'new password and confirm password must be same')

        else:
            messages.error(request, 'Enter valid current password')


    return render(request, 'change_password.html', context=student_dict)


def admin_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if Admin.objects.filter(admin_username__exact=username, admin_password__exact=password).count() == 1:
            
            admin = Admin.objects.filter(admin_username__exact=username, admin_password__exact=password).get()

            request.session['admin_id'] = str(admin.id)
            return HttpResponseRedirect(reverse('admin_index'))
        
        else:
            messages.info(request, 'Invalid login details!!')
    return render(request, 'admin_login.html', context=None)



@myadmin_login_required
def admin_index(request):

    student_count = 0
    if Student.objects.values('student_college_id').filter(student_approve=False).order_by('student_college_id').count() > 0:

        student_list = Student.objects.values('student_college_id').filter(student_approve=False).order_by('student_college_id')
        student_count = Student.objects.values('student_college_id').filter(student_approve=False).order_by('student_college_id').count()
        print(student_list[0]['student_college_id'])
        print(student_count)
        i=0
    
    student_result = []

    if student_count > 0:
        while i<student_count:
            student_result.append(student_list[i]['student_college_id'])
            i = i + 1

    print(student_result)

    student = {'student_result':student_result}

    if request.method == 'POST':
        
        if request.POST.get('approve_selected') == 'Approve Selected':

            choices = request.POST.getlist('student_approve')
            print(choices)
            
            for choice in choices:
                Student.objects.filter(student_college_id__exact=choice).update(student_approve=True)
            
            return HttpResponseRedirect('admin_index')

        else:
            Student.objects.filter(student_approve=False).update(student_approve=True)
            return HttpResponseRedirect('admin_index')


    return render(request, 'admin_index.html', context=student)


@myadmin_login_required
def admin_add_subject(request):


    if request.method == 'POST':

        admin_id = request.session['admin_id']
        subject_name = request.POST.get('subject_name', '').lower()
        subject_semester = int(request.POST.get('subject_semester', ''))

        print(subject_semester)
        print(subject_name)

        subject_add = Subject.objects.create(subject_name=subject_name, subject_semester=subject_semester)
        subject_add.save()
 

    return render(request, 'admin_add_subject.html', context=None)


@myadmin_login_required
def admin_view_subject(request):

    subjects = Subject.objects.values('subject_name', 'subject_semester').order_by('subject_semester')
    print(subjects)

    dictionary = {'subjects':subjects}

    for subject in dictionary['subjects']:
        print(subject['subject_name'])


    if request.method == 'POST':
        if request.POST.get('delete_selected') == 'Delete Selected':

            choices = request.POST.getlist('subject_delete')
            print(choices)

            for choice in choices:
                Subject.objects.filter(subject_name=choice).delete()

            return HttpResponseRedirect('admin_view_subject')

        else:

            Subject.objects.delete()
            return HttpResponseRedirect('admin_view_subject')

    return render(request, 'admin_view_subject.html', context=dictionary)


@myadmin_login_required
def admin_result(request):

    day = get_day()
    month = get_month()
    year = get_year()

    results = Result.objects.values('result_subject', 'result_semester', 'result_year').order_by('result_semester').filter(result_year=int(get_year()))
    print('result: ', results)
    dictionary = {'results':results}

    return render(request, 'admin_result.html', context=dictionary)


def admin_statistics(request):

    result = Result.objects.values('result_subject', 'result_semester', 'result_year').filter(result_year=int(get_year())-1).order_by('result_semester')
    dictionary = {'results':result}

    return render(request, 'admin_statistics.html', context=dictionary)


def admin_about(request):

    return render(request, 'admin_about.html', context=None)