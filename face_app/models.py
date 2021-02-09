from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):

	YEAR_IN_SCHOOL_CHOICES = [
		('Freshman', 'Freshman'),
		('Sophomore', 'Sophomore'),
		('Junior', 'Junior'),
		('Senior', 'Senior')
    ]

	MAJOR_CHOICES = [
		('English', 'English'),
		('Business Administration', 'Business Administration'),
		('Teaching', 'Teaching'),
		('Information Technology', 'Information Technology'),
		('Christian Studies', 'Christian Studies'),
		('Bioscience', 'Bioscience'),
		('Public Health', 'Public Health')
	]

	firstname = models.CharField(max_length = 100)
	lastname = models.CharField(max_length = 100)
	student_id = models.CharField(max_length = 9, unique = True)
	year = models.CharField(max_length = 10, choices = YEAR_IN_SCHOOL_CHOICES, default = 'Freshman')
	major = models.CharField(max_length = 25, choices = MAJOR_CHOICES, default = 'English')

	def __str__(self):
		return self.firstname + ' ' + self.lastname + ':' + self.student_id


	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('students')
		
class Face(models.Model):
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	image = models.ImageField(null = True, blank = True, default = 'default-user.png')

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('students')

	@property
	def imageURL(self):
		try:
		 	url = self.image.url
		except:
		 	url = ''
		return url 

class Encoding(models.Model):
	face = models.OneToOneField(Face, on_delete = models.CASCADE)
	encoding = models.BinaryField()

class ClassCourse(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	course_id = models.CharField(max_length = 10)
	start = models.TimeField(null=True)
	end = models.TimeField(null=True)

	def __str__(self):
		return self.name

class Attendance(models.Model):
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	classcourse = models.ForeignKey(ClassCourse, on_delete = models.CASCADE, null=True)
	date = models.DateField(null=True)
	time = models.TimeField(null=True)
	entry = models.CharField(max_length = 5)

class ClassDay(models.Model):
	classcourse = models.ForeignKey(ClassCourse, on_delete=models.CASCADE)
	day = models.CharField(max_length = 10,null=True)
		
class StudentEnrollClass(models.Model):	
	student = models.ForeignKey(Student, on_delete = models.CASCADE)
	classcourse = models.ForeignKey(ClassCourse, on_delete = models.CASCADE)
	
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('class')