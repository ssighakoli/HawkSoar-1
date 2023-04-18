from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from db_connect.forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from db_connect.filters import CourseFilter

#HELPER FUNCTIONS
def get_user(user):
    if user.user_type == 'student':
        return Student.objects.get(user_id=user.id)
    if user.user_type == 'mentor':
        return Mentor.objects.get(user_id=user.id)
    if user.user_type == 'tutor':
        return Tutor.objects.get(user_id=user.id)
    
def get_events(request):
    user = get_user(request.user)
    has_events = list(Has_Events.objects.filter(id=user.id)) #this returns a list of Has_Events objects that match the users id
    print(has_events)
    events = []
    for e in has_events: #for each Has_Event object in 'has_events' we get the Event object from the Events table in our db
        events.append(Events.objects.get(pk=e.event_id.pk))
    return events
#HELPER FUNCTIONS (END)

#SIGN UP AND LOGIN/LOGOUT VIEWS INCLUDING ROLE MANAGER (DIRECTS USERS TO THEIR DASHBOARD)
def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            userType = form.cleaned_data['user_type']
            if userType not in ['student', 'tutor', 'mentor']:
                return HttpResponseBadRequest("Invalid user type")
            
            name = form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            cwid = request.POST.get('cwid')
            major = request.POST.get('major')
            user = form.save() #user instance is posted to db auth_user
            if userType == 'student':
                student = Student.objects.create(user=user, A_number=cwid, Student_Name=name, Student_email=email, Major=major)
                student.save()
                return redirect('course_quantity', cwid)
            if userType == 'tutor':
                tutor = Tutor.objects.create(user=user, Tid=cwid, email=email)
                tutor.save()
                return redirect('tutor_course', cwid)
            if userType == 'mentor':
                mentor = Mentor.objects.create(user=user, Mid=cwid, name=name, email=email)
                mentor.save()
            
            return redirect('login_view')
    else:
        form = UserSignUpForm()
    return render(request, 'user_signup.html', {'form': form})    

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email') #get the email from the login html form
        password = request.POST.get('password') #get the pw from the login html form
        user = authenticate(request, email=email, password=password) #authenticate the user by checking the credentials in the user_register table
        if user is not None:
            login(request, user) #if they exists create a new session and log them in
            return redirect('role_manager') #redirect them to the events they've signed up for
        else:
            messages.error(request, 'Invalid email or password. Please Try Again')
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required
def role_manager(request):
    user_role = request.user.user_type
    user = get_user(request.user)
    if user_role == 'student':
        return redirect('student', user_id=request.user.id)
    elif user_role == 'tutor':
        return redirect('tutor', user_id=request.user.id)
    elif user_role == 'mentor':
        return redirect('mentor', user_id=request.user.id)
    else:
        return HttpResponseBadRequest("Invalid user type")
#END

#VIEWS THAT RENDER THE CORRESPONDING DASHBOARD PAGES FOR EACH USER
@login_required
def student(request, user_id):
    user = get_user(request.user)
    events = get_events(request)
    return render(request, 'student_home.html', {'user': user, 'events': events})

@login_required
def tutor(request, user_id):
    user = get_user(request.user)
    #print(user.Tid)
    # students = Student.objects.all()
    cids = []
    for object in TutorsCourse.objects.filter(Tid=user.id):
        cids.append(object.course_id)
    print(cids)
    students = []
    for cid in cids:
        course = Course_Registered.objects.get(Course_id=cid)
        if course.Course_id == cid:
            students.append([course.A_number.Student_Name, course.A_number.A_number, course.Course_Name])  
    print(students)
    return render(request, 'tutor_home.html', {'user': user, 'students': students})

@login_required
def mentor(request, user_id):
    user = get_user(request.user)
    return render(request, 'mentor_home.html', {'user': user})
#END


#####################################
#VIEWS FOR ANY USER TO USE (excepts students can't use event_create)
#####################################
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.user_type == 'tutor':
                return redirect('tutor')
            if request.user.user_type == 'mentor':
                return redirect('mentor')
    else:
        form = EventForm()
    return render(request, 'event_create.html', {'form': form})

@login_required
def collaboration_portal(request):
    #this would allow users to look up other users in the database and connect with them
    pass
#####################################
#VIEWS FOR ANY USER (END)
#####################################


#STUDENT VIEWS


@login_required
def event_signup(request, user_id):
    events = Events.objects.all()
    user = get_user(request.user)
    print("GOT USER PROFILE,", user)
    if request.method == 'POST':
        event_pk = request.POST.get('event')
        event = Events.objects.get(pk=event_pk)
        has_events = Has_Events(A_number=user, event_id=event, event_name=event, event_date=event)
        has_events.save()
        return redirect('student', user_id)
    return render(request, 'event_signup.html', {'events': events})

def course_quantity(request, A_number):
    if request.method == 'POST':
        num_courses = int(request.POST.get('num_courses'))
        return redirect('register_courses', A_number, num_courses)
    return render(request, 'course_quantity.html')

#User signs up -> User selects number of course they're taking in course_quantity() -> register_courses()
def register_courses(request, A_number, extra):
    CourseFormSet = formset_factory(CoursesForm, extra=extra)
    if request.method == 'POST':
        formset = CourseFormSet(request.POST)
        if formset.is_valid():
            student = Student.objects.get(A_number=A_number)
            for form in formset:
                course_id = form.cleaned_data.get('Course_id')
                course_name = form.cleaned_data.get('Course_Name')
                course = Course_Registered.objects.create(A_number=student, Course_id=course_id, Course_Name=course_name)
                course.save()
            return redirect('login_view')
    else:
        formset = CourseFormSet()
    return render(request, 'course_register.html', {'formset': formset, 'A_number': A_number})

@login_required
def my_assignments(request, user_id):
    pass
@login_required
def my_schedule(request, user_id):
    pass
@login_required
def performance_report(request, user_id):
    pass
#STUDENT VIEWS (END)

#TUTOR VIEWS
def tutor_course(request, Tid):
    if request.method == 'POST':
        tutor = Tutor.objects.get(Tid=Tid)
        course_ids_list = request.POST.getlist('courses[]')
        for course_string in course_ids_list:
            cin, cname = course_string.split('-') #get id and name, by splitting '-' between the course_id variable
            tutor_course = TutorsCourse.objects.create(Tid=tutor, course_id=cin, cname=cname)
            tutor_course.save()
        return redirect('login_view')
    else:
        courses = Course_Registered.objects.all()
        myFilter = CourseFilter(request.GET, queryset=courses)
        courses = myFilter.qs
        context = { 'courses':courses, 'myFilter':myFilter }
        return render(request, 'tutor_course.html', context)

@login_required
def assign_group(request):
    pass
@login_required
def assignment_manager(request, user_id):
    pass
@login_required
def performance_manager(request, user_id):
    pass
@login_required
def submit_feedback(request):
    pass
#TUTOR VIEWS (END)

#MENTOR VIEWS
@login_required
def meeting_scheduler(request, user_id):
    pass
#MENTOR VIEWS (END)






# def user_registation(request):
#     if request.method == 'POST':
#         form = User_register_Form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login_view')
#     else:
#         form = User_register_Form()
#     return render(request, 'user_registration.html', {'form': form})


# Create your views here.
# def index(request):
#     return HttpResponse("Welcome to HawkSoar Application")


