from django.shortcuts import render,redirect,HttpResponseRedirect#,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse
from django.core.exceptions import *
import datetime
import face_recognition
import requests
import pickle
import base64
from io import BytesIO
from .webcam import *
from .models import *
from .forms import *

# Student CRUD
class ListDeleteStudent(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = ('face_app.delete_student', 'face_app.view_student', 'face_app.add_encoding')
	def post(self, request, *args, **kwargs):
		students_id = request.POST.getlist('id[]')
		for id in students_id:
			student = Student.objects.get(student_id=id)
			student.delete()
		return redirect('students')

	def get(self, request, *args, **kwargs):
		encodings = []
		face_id = []
		message = request.GET.get('message')
		if message == "face_encode":
			face = Face.objects.all()
			for face in face:
				Encoding.objects.all().delete()
				face_id.append(face.id)
				server = "http://127.0.0.1:8000"
				url = face.imageURL
				image = server+url
				response = requests.get(image)
				img = BytesIO(response.content)
				person = face.imageURL.split('/')[2]
				person = person.split('.')[0]
				person = person.replace("_"," ")
				# Get the face encodings for the face in each image file
				face = face_recognition.load_image_file(img)
				face_bounding_boxes = face_recognition.face_locations(face)
				#If training image contains exactly one face
				if len(face_bounding_boxes) == 1:
				    face_enc = face_recognition.face_encodings(face)[0]
				    # Add face encoding for current image with corresponding label (name) to the training data
				    encodings.append(face_enc)
				else:
				    print(face.imageURL+ " was skipped and can't be used for training")
			for e,f in zip(encodings,face_id):
				# converting numpy array to binary
				np_bytes = pickle.dumps(e)
				np_base64 = base64.b64encode(np_bytes)
				face = Face.objects.get(id = f)
				encoding = Encoding.objects.create(face = face, encoding = np_base64)
				encoding.save()

		students = Student.objects.all()
		context = {'object_list':students}
		return render(request, "face_app/students.html", context)

class StudentDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	login_url = 'login'
	permission_required = 'face_app.view_student'
	model = Student
	template_name = 'face_app/student_detail.html'

@login_required(login_url='login')
@permission_required('face_app.view_face')
def studentFaceDetail(request,pk):
	face = None
	try:
		face = Face.objects.filter(student=pk)
		if not face:
			face = ['']
	except ObjectDoesNotExist:
		face = ""
	finally:
		context = {'face' : face}
		return render(request, 'face_app/studentface_detail.html', context)		
		
class CreateStudent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	login_url = 'login'
	permission_required = 'face_app.add_student'
	model = Student
	form_class = CreateStudentForm 
	template_name = 'face_app/create_student.html'
	success_url = 'add_face'

class UpdateStudent(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	login_url = 'login'
	permission_required = 'face_app.change_student'
	model = Student
	form_class = UpdateStudentForm 
	template_name = 'face_app/update_student.html'

class AddStudentFace(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	login_url = 'login'
	permission_required = 'face_app.add_face'
	model = Face
	form_class = AddStudentFace 
	template_name = 'face_app/add_face.html'

# ====================================================================================
# Class CRUD
@login_required(login_url='login')
@permission_required('face_app.add_classcourse','face_app.add_classday')
def createClass(request, *args):
	user = request.user
	user = User.objects.get(username=user)
	if request.method == 'POST':
		day = request.POST.getlist('day')
		start = request.POST.get('start')
		end = request.POST.get('end')
		class_name = request.POST.get('class_name')
		class_id = request.POST.get('class_id')
		classCourse = ClassCourse(name=class_name, course_id=class_id, user=user, start=start, end=end)
		classCourse.save()
		for day in day:
			classDay  = ClassDay(classcourse=classCourse, day=day)
			classDay.save()
		return redirect('class')
	return render(request, 'face_app/create_class.html')

class EnrollStudent(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = 'face_app.add_studentenrollclass'
	def post(self, request, *args, **kwargs):
		students_id = request.POST.getlist('id[]')
		course = request.POST.get('classname')
		classcourse = ClassCourse.objects.get(course_id=course)
		for id in students_id:
			student = Student.objects.get(student_id=id)
			studentEnroll = StudentEnrollClass(student = student, classcourse = classcourse)
			studentEnroll.save()
		return redirect('class')

	def get(self, request):
		courses = ClassCourse.objects.all()
		students = Student.objects.all()
		context = {'object_list':students, 'courses':courses}
		return render(request, 'face_app/enroll_student.html', context)

class UpdateClassCourse(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = ('face_app.change_classcourse','face_app.change_classday')
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		name = request.POST.get('class_name')
		course_id = request.POST.get('class_id')
		day = request.POST.getlist('day')
		start = request.POST.get('start')
		end = request.POST.get('end')
		classcourse = ClassCourse.objects.filter(id=id).update(
			name=name,start=start,end=end, course_id=course_id)
		cc = ClassCourse.objects.get(course_id=course_id)
		classday = ClassDay.objects.filter(classcourse=cc)
		dlen = len(day)
		cdlen = len(classday)
		count = 0
		if dlen == cdlen:
			for day,cd in zip(day,classday):
				if day != cd.day:
					updateday = ClassDay.objects.filter(id=cd.id)
					updateday.update(day=day)
		elif dlen > cdlen:
			for d,cd in zip(day,classday):
				if d != cd.day:
					count = count + 1
					updateday = ClassDay.objects.filter(id=cd.id)
					updateday.update(day=d)
			while count < dlen:
				d = day[count]
				ClassDay.objects.create(classcourse=cc, day=d)
				count = count + 1

		elif dlen < cdlen:
			clsday = []
			for cld in classday:
				clsday.append(cld.id)
			for d,cd in zip(day,classday):
				if d != cd.day:
					count = count + 1
					updateday = ClassDay.objects.filter(id=cd.id)
					updateday.update(day=d)
				elif d == cd.day:
					count = count + 1
			while count < cdlen and count != 0:
				clsid = clsday[count]
				ClassDay.objects.get(id=clsid).delete()
				count = count + 1

		return redirect('class')

	def get(self, request, pk):
		classcourse = ClassCourse.objects.filter(id=pk)
		context = {'classcourse':classcourse}
		return render(request, 'face_app/update_class.html', context)

class ListDeleteClass(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = ('face_app.delete_classcourse', 'face_app.view_classcourse',
		'face_app.delete_classday', 'face_app.view_classday')	
	def post(self, request, *args, **kwargs):
		if request.method == 'POST':
			course_id = request.POST.getlist('id[]')
			for id in course_id:
				student = ClassCourse.objects.get(id=id)
				student.delete()
			return redirect('class')

	def get(self, request):
		user = request.user
		user = User.objects.get(username=user)
		classcourse = ClassCourse.objects.filter(user=user)
		classday = []
		for c in classcourse:
			classday.append(ClassDay.objects.filter(classcourse=c))
		object_list = zip(classcourse,classday)
		context = {'object_list':object_list}
		return render(request, "face_app/class.html", context)

class ClassDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = ['face_app.view_studentenrollclass','face_app.delete_studentenrollclass']
	def get(self, request, pk):
		course = ClassCourse.objects.get(id=pk)
		studentenrollclass = StudentEnrollClass.objects.filter(classcourse=course)
		students = Student.objects.filter(studentenrollclass__in=studentenrollclass)
		context = {'students':students, 'course':course}
		return render(request, 'face_app/class_detail.html', context)

	def post(self, request, *args, **kwargs):
		student_id = request.POST.getlist('id[]')
		class_id = request.POST.get('classcourse')
		for id in student_id:
			s = Student.objects.get(id=id)
			cc = ClassCourse.objects.get(id=class_id)
			se = StudentEnrollClass.objects.get(student=s, classcourse=cc)
			se.delete()
		return redirect('/class_detail/'+class_id)
# ====================================================================================
# Attendance CRUD
@login_required(login_url='login')
@permission_required('face_app.add_attendance')
def createAttendance(request, *args, **kwargs):
	if request.method == 'POST':
		class_id = request.POST.get('course_id')
		student_list = request.POST.getlist('student_id')
		att_list = request.POST.getlist('attendance')
		classcourse = ClassCourse.objects.get(course_id=class_id)
		date = datetime.date.today()
		endtime = classcourse.end
		endtime = endtime.strftime("%H:%M") 
		for student,att in zip(student_list,att_list):
			if att == "present":
				starttime = classcourse.start
				starttime = starttime.strftime("%H:%M") 
				student = Student.objects.get(student_id=student)
				attendanceEntry = Attendance(student=student, classcourse=classcourse, 
					date=date, time=starttime, entry='enter')
				attendanceEntry.save()
				attendanceExit = Attendance(student=student, classcourse=classcourse, 
					date=date, time=endtime, entry='exit')
				attendanceExit.save()
			elif att == "tardy":
				starttime = (datetime.datetime.combine(datetime.date.today(), classcourse.start)
					+datetime.timedelta(minutes=5))
				starttime = starttime.strftime("%H:%M")
				student = Student.objects.get(student_id=student)
				attendanceEntry = Attendance(student=student, classcourse=classcourse, 
					date=date, time=starttime, entry='enter')
				attendanceEntry.save()
				attendanceExit = Attendance(student=student, classcourse=classcourse, 
					date=date, time=endtime, entry='exit')
				attendanceExit.save()
			elif att == "absent":
				student = Student.objects.get(student_id=student)
				attendanceEntry = Attendance(student=student, classcourse=classcourse, 
					date=date, entry='enter')
				attendanceEntry.save()
				attendanceExit = Attendance(student=student, classcourse=classcourse, 
					date=date, entry='exit')
				attendanceExit.save()
		return redirect('attendance')

	if request.method == 'GET':
		class_id = request.GET.get('class_id')
		classcourse = ClassCourse.objects.get(course_id=class_id)
		sec = StudentEnrollClass.objects.filter(classcourse=classcourse) 
		students = Student.objects.filter(studentenrollclass__in=sec)
		context = {'students':students,'classcourse':classcourse}
	return render(request, 'face_app/create_attendance.html', context)

@login_required(login_url='login')
@permission_required('face_app.view_classcourse')
def selectClass(request):
	if request.method == 'GET':
		context={}
		classcourse = ClassCourse.objects.all()
		context["classcourse"]=classcourse
	return render(request, 'face_app/select_class.html', context)
		
class ListDeleteAttendance(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = ('face_app.delete_attendance', 'face_app.view_attendance')	
	def post(self, request, *args, **kwargs):
		attendance_id = request.POST.getlist('id[]')
		print(attendance_id)
		for id in attendance_id:
			att = Attendance.objects.get(id=id)
			att.delete()
		return redirect('attendance')

	def get(self, request, *args, **kwargs):
		listclass = ClassCourse.objects.all()
		course_id = request.GET.get('course_id')
		attendance = None
		classcourse = None
		if course_id:
			classcourse = ClassCourse.objects.get(course_id=course_id)
			attendance = Attendance.objects.filter(classcourse=classcourse)
		context={'attendance':attendance, 'listclass':listclass, 'classcourse': classcourse}
		return render(request, "face_app/attendance.html",context)

class UpdateAttendance(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = 'login'
	permission_required = 'face_app.change_attendance'
	def post(self, request, *args, **kwargs):
		id = request.POST.get('id')
		time = request.POST.get('time')
		attendance = Attendance.objects.filter(id=id).update(time=time)
		return redirect('attendance')

	def get(self, request, pk):
		attendance = Attendance.objects.filter(id=pk)
		context = {'attendance':attendance}
		return render(request, 'face_app/update_attendance.html', context)
# ====================================================================================
# login logout
def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username or password is incorrect')

	return render(request, 'face_app/login.html')

def logout_user(request):
	logout(request)
	return redirect('login')
# ====================================================================================
# reset password
class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
	login_url = 'login'
	form_class = PasswordChangeForm
	template_name = "face_app/password_change.html"
	success_url = reverse_lazy('reset_password_done')

class PasswordResetDoneView(LoginRequiredMixin, PasswordResetDoneView):
	login_url = 'login'
	template_name = "face_app/password_reset_done.html"

# ====================================================================================
# cameras, hopefully good quality :D
cam1 = VideoCamera1()
cam2 = VideoCamera2()

def frame(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

async def webcam1(request):
	while True:
		return StreamingHttpResponse(frame(cam1), 
		content_type='multipart/x-mixed-replace; boundary=frame')
	
async def webcam2(request):
	while True:
		return StreamingHttpResponse(frame(cam2), 
		content_type='multipart/x-mixed-replace; boundary=frame')
# ====================================================================================
# live web cams
@login_required(login_url='login')
def live(request, *args):
	studentenroll = []
	
	if request.method == 'POST':
		classname = request.POST.get('class')
		classcourse = ClassCourse.objects.get(id=classname)
		studentenroll = StudentEnrollClass.objects.filter(classcourse=classcourse)
		for se in studentenroll:
			print(se.student)

	classname = ClassCourse.objects.all()
	context = {'classname':classname}
	return render(request, 'face_app/live.html',context)
# ====================================================================================
# dashboard
def entryTime(time):
    t = datetime.datetime.strptime(time, '%H:%M').time()
    t = t.strftime('%H:%M')
    tmp = t.split(':')
    hour = int(tmp[0])
    minute = int(tmp[1])
    t = datetime.timedelta(hours=hour, minutes=minute)
    return t

def calTime(student):
    for s in student:
        date = student[s]
        total = datetime.timedelta()
        for d in date:
            entry = date[d]
            enter = entry['enter']
            exit = entry['exit']
            result = datetime.timedelta()
            for enter, exit in zip(enter, exit):
                t1 = entryTime(enter)
                t2 = entryTime(exit)
                result = result + (t2 - t1)
            total = total + result
        count = len(date)
        return s, total, count

# present, tardy, absent
def pta(list, att_id):
    attendance = Attendance.objects.get(id=att_id)
    classcourse = ClassCourse.objects.get(attendance=attendance)
    start = classcourse.start
    hour = start.strftime("%H")
    minute = start.strftime("%M")
    present = datetime.timedelta(hours=int(hour), minutes=int(minute))
    tardy = datetime.timedelta(hours=int(hour), minutes=int(minute)+5)
    absent = datetime.timedelta(hours=int(hour), minutes=int(minute)+10)
    none = datetime.timedelta(hours=0, minutes=0)
    pta = {}
    for tmp in list:
        for t in tmp:
            tm = datetime.datetime.strptime(tmp[t], '%H:%M').time()
            tm = tm.strftime('%H:%M')
            tmp = tm.split(':')
            hour = int(tmp[0])
            minute = int(tmp[1])
            tm = datetime.timedelta(hours=hour, minutes=minute)
            if present <= tm < tardy:
                pta[t] = 'present'
            elif tardy <= tm < absent:
                pta[t] = 'tardy'
            elif tm > absent or tm == none:
                pta[t] = 'absent'
    return pta

@login_required(login_url='login')
def dashboard(request, *args, **kwargs):
	if request.method == 'GET':
		listclass = []
		student_list = []
		studentName = set()
		stdpta = {}
		user = request.user
		user = User.objects.get(username=user)
		classcourse = ClassCourse.objects.filter(user=user)
		clc = None
		# referencing students' attendance by date and time
		for cc in classcourse:
			listclass.append(cc)
		if request.GET:
			course_id = request.GET.get('course_id')
			clc = ClassCourse.objects.get(course_id=course_id)
			ctime = clc.start
			att = Attendance.objects.filter(classcourse=clc)
			for a in att:
				studentName.add(str(a.student))
			studentName = sorted(list(studentName))
			for sn in studentName:
				student_id = sn.split(':')[1]
				std = Student.objects.get(student_id=student_id)
				attendance = Attendance.objects.filter(classcourse=clc, student=std)
				tmps = set()
				date = {}
				tmppta = []
				tmpatt = int()
				for a in attendance:
					tmps.add(a.date)
				for ts in tmps:
					attendance = Attendance.objects.filter(classcourse=clc, student=std, date=ts)			
					enter = []
					exit = []
					entry = {}
					for i, a in enumerate(attendance):
						time = a.time
						if time is None:
							if a.entry == 'enter':
								enter.append('00:00')
								if i == 0:
									tmp = {str(ts): '00:00'}
									tmppta.append(tmp)
							elif a.entry == 'exit':
								exit.append('00:00')
						else:
							if a.entry == 'enter':
								time = time.strftime("%H:%M")
								enter.append(time)
								if i == 0:
									tmp = {str(ts): time}
									tmppta.append(tmp)
									tmpatt = a.id
							elif a.entry == 'exit':			
								time = time.strftime("%H:%M")
								exit.append(time)

					

					entry['enter'] = enter
					entry['exit'] = exit
					date[str(ts)] = entry
				
				stdpta[sn] = pta(tmppta, tmpatt)
				
				student = {sn: date}					
				student_list.append(student)

		# default time 1 hour & 50 minutes
		realtime = datetime.timedelta(hours=1, minutes=50)

		# attendance percentage from day 1 until today
		att_per = {}
		for student in student_list:
			s, caltime, count = calTime(student)
			rtime = realtime * count
			result = (caltime * 100) / rtime
			result = float(result)
			result = round(result, 2)
			if caltime >= rtime:
				att_per[s] = 100
			else:
				att_per[s] = result

		# attendance percentage per semester
		sem_per = {}
		semtime = realtime * 30
		for student in student_list:
			s, caltime, count = calTime(student)
			result = (caltime * 100) / semtime
			result = float(result)
			result = round(result, 2)
			if caltime >= semtime:
				sem_per[s] = 100
			else:
				sem_per[s] = result


		context = {'listclass': listclass, 'att_per': att_per, 'sem_per': sem_per,
		'clc': clc, 'stdpta': stdpta}
		return render(request, 'face_app/dashboard.html', context)