import django_filters
from django_filters import FilterSet, CharFilter #requires 'pip install django-filter' while in virtual environment

from db_connect.models import *

class CourseFilter(django_filters.FilterSet):
    Course_id = CharFilter(field_name='Course_id', lookup_expr='icontains')
    class Meta:
        model = Course_Registered
        fields = '__all__'
        exclude = ['A_number', 'Course_Name']

class StudentFilter(django_filters.FilterSet):
    Student_Name = CharFilter(field_name='Student_Name', lookup_expr='icontains')
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'A_number']