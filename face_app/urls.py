from django.urls import path
from . import views


urlpatterns = [
	path('students/', views.ListDeleteStudent.as_view(), name='students'),
	path('create_student/', views.CreateStudent.as_view(), name='create_student'),
	path('create_student/add_face', views.AddStudentFace.as_view(), name='add_face'),
	path('update_student/<int:pk>', views.UpdateStudent.as_view(), name='update_student'),
	path('class/', views.ListDeleteClass.as_view(), name='class'),
	path('update_class/<int:pk>', views.UpdateClassCourse.as_view(), name='update_class'),
	path('create_class/', views.createClass, name='create_class'),
	path('enroll_student/', views.EnrollStudent.as_view(), name='enroll_student'),
	path('class_detail/<int:pk>', views.ClassDetail.as_view(), name='class_detail'),
	path('', views.login_user, name='login'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('logout/', views.logout_user, name='logout'),
	path('student_detail/<int:pk>', views.StudentDetail.as_view(), name='student_detail'),
	path('studentface_detail/<int:pk>', views.studentFaceDetail, name='studentface_detail'),
	path('attendance/', views.ListDeleteAttendance.as_view(), name='attendance'),
	path('select_class/', views.selectClass, name='select_class'),
	path('create_attendance/', views.createAttendance, name='create_attendance'),
	path('update_attendance/<int:pk>', views.UpdateAttendance.as_view(), name='update_attendance'),
	path('live/', views.live, name='live'),
	path('webcam1/', views.webcam1, name='webcam1'),
	path('webcam2/', views.webcam2, name='webcam2'),
	path('change_password/', views.PasswordChangeView.as_view(), name='change_password'),
	path('change_password/done/', views.PasswordResetDoneView.as_view(), name='reset_password_done')
]