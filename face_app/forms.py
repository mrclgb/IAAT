from django import forms 
from django.contrib.auth.forms import PasswordChangeForm
from .models import *

class CreateStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		widgets = {
			'firstname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'lastname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'student_id': forms.TextInput(attrs={'class':'form-control text-light','pattern':'[0-9]+',
			'placeholder': 'Numbers only!'}),
			'year': forms.Select(attrs={'class':'form-control text-light'}),
			'major': forms.Select(attrs={'class':'form-control text-light'})
		}

class AddStudentFace(forms.ModelForm):
	class Meta:
		model = Face
		fields = ['student','image']
		widgets = {
			'image': forms.FileInput(attrs={'class':'form-control text-light'}),
			'student': forms.Select(attrs={'class':'form-control text-light'})
		}

class UpdateStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		widgets = {
			'firstname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'lastname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'student_id': forms.TextInput(attrs={'class':'form-control text-light','pattern':'[0-9]+',
			'placeholder': 'Numbers only!'}),
			'year': forms.Select(attrs={'class':'form-control text-light'}),
			'major': forms.Select(attrs={'class':'form-control text-light'})
		}

class UpdateStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		widgets = {
			'firstname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'lastname': forms.TextInput(attrs={'class':'form-control text-light'}),
			'student_id': forms.TextInput(attrs={'class':'form-control text-light','pattern':'[0-9]+',
			'placeholder': 'Numbers only!'}),
			'year': forms.Select(attrs={'class':'form-control text-light'}),
			'major': forms.Select(attrs={'class':'form-control text-light'})
		}

class PasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control text-light', 'type':'password'}))
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control text-light', 'type':'password'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control text-light', 'type':'password'}))
		
