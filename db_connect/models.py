from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

# Extending the base User manager that Django uses for its original UserManager.
# Defining the same 3 methods that the original Django UserManager has.
# Not using username in either of those methods.
# Validating that email is provided when creating a User.
# Assigning the new Manager to the User model.
class UserManager(BaseUserManager):
    #Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        #Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        #Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        #Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLES = (
        ('', 'Select Your Role'),
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('mentor', 'Mentor'),
    )
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=10, choices=ROLES, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    Tid = models.CharField(max_length = 9)
    email = models.CharField(max_length = 100)

class TutorsCourse(models.Model):
    Tid = models.ForeignKey(Tutor,on_delete=models.CASCADE,default='')
    course_id = models.CharField(max_length=10)
    cname = models.CharField(max_length = 20)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="")
    Mid = models.CharField(max_length = 9)
    name = models.CharField(max_length = 20)
    email = models.CharField(max_length = 100)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    A_number = models.CharField(max_length = 9)
    Student_Name = models.CharField(max_length = 20)
    Student_email = models.EmailField()
    Major = models.CharField(max_length = 50)

class Mentees(models.Model):
    Mid = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    A_number = models.ForeignKey(Student, on_delete=models.CASCADE)

class Assignments(models.Model):
    A_number = models.ForeignKey(Student, on_delete = models.CASCADE)
    Tid = models.ForeignKey(Tutor, on_delete = models.CASCADE, related_name= 'Tutor_id')
    Assignment_Name = models.CharField(max_length= 10)
    # from datetime import date
    # from myapp.models import MyModel

    # my_date = date(2022, 5, 15)
    # my_instance = MyModel(Due_Date=my_date)
    Due_Date = models.DateField(null=True)
    Description = models.CharField(max_length = 20)
    Attach = models.CharField(max_length = 10)
    Submit_Status = models.CharField(max_length = 20, default="Not Submitted")

class Events(models.Model):
    event_name = models.CharField(max_length = 20)
    event_date = models.DateTimeField(null=True)

class Has_Events(models.Model):
    A_number = models.ForeignKey(Student,on_delete = models.CASCADE,related_name = 'Student_number')
    event_id = models.ForeignKey(Events, on_delete = models.CASCADE, related_name = 'Eid')
    event_name = models.ForeignKey(Events, on_delete = models.CASCADE,related_name = 'Ename')
    event_date = models.ForeignKey(Events,on_delete = models.CASCADE,related_name = 'Edate')

class Course_Registered(models.Model):
    A_number = models.ForeignKey(Student,on_delete = models.CASCADE, related_name = 'CWID')
    Course_id = models.CharField(max_length = 10)
    Course_Name = models.CharField(max_length = 20)

class Performance(models.Model):
    A_number = models.ForeignKey(Student,on_delete = models.CASCADE)
    Course_id = models.ForeignKey(Course_Registered,on_delete = models.CASCADE)
    OverallGPA = models.FloatField()
    Grade = models.CharField(max_length = 2)
    Feedback = models.TextField()

class Group(models.Model):
    GID = models.CharField(max_length = 4)
    A_number = models.ForeignKey(Student,on_delete = models.CASCADE)
    CID = models.CharField(max_length=10)
    GName = models.CharField(max_length=10)

class MentorMeeting(models.Model):
    Mid = models.ForeignKey(Mentor, on_delete = models.CASCADE)
    A_number = models.ForeignKey(Student, on_delete = models.CASCADE)
    mName = models.CharField(max_length=25)
    mDate = models.DateTimeField(null=True)

class MenteeMessage(models.Model):
    A_number = models.ForeignKey(Mentees, on_delete=models.CASCADE)
    Mid = models.ForeignKey(Mentees, on_delete=models.CASCADE, related_name='Mentor_ID')
    Message = models.TextField(null=False, max_length=1000)
    M_Date = models.DateField(auto_now_add=True)


