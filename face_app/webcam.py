import face_recognition
import cv2
import numpy as np
import pickle
import base64
from .models import *
import datetime


class VideoCamera1(object):
	def __init__(self, index=0):
		self.video = cv2.VideoCapture(index)
		print(self.video.isOpened())
	    
	def _del_(self):
		self.video.release()
	    
	def get_frame(self,in_graysale=False):
		# Initialize some variables
		face_locations = []
		face_encodings = []
		
		process_this_frame = True

		known_face_encodings = []
		known_face_names = []

		# query name and face encodings from the database
		enc = Encoding.objects.all()
		for e in enc:
			id = e.id
			encoding = Encoding.objects.get(id=id)
			face = Face.objects.get(encoding=encoding)
			name = Student.objects.get(face=face)
			encodings = base64.b64decode(encoding.encoding)
			encodings = pickle.loads(encodings)
			known_face_encodings.append(encodings)
			known_face_names.append(str(name))

		# check today class
		day = datetime.datetime.today().strftime("%A")
		time = datetime.datetime.today().strftime("%H:%M")
		studentsInClass = []
		class_id = None
		cd = ClassDay.objects.filter(day=day)
		for cd in cd:
			cc = ClassCourse.objects.get(classday=cd)
			start = cc.start
			start = start.strftime("%H:%M")
			end = cc.end
			end = end.strftime("%H:%M")
			# check if a student is detected during this time
			if time >= start and time <=end:
				class_id = cc.id
				se = StudentEnrollClass.objects.filter(classcourse=cc)
				for se in se:
					student = str(se.student)
					studentsInClass.append(student)

		while True:
			# Grab a single frame of video
			ret, frame = self.video.read()

			# Resize frame of video to 1/4 size for faster face recognition processing
			small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

			# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
			rgb_small_frame = small_frame[:, :, ::-1]

			# Only process every other frame of video to save time
			if process_this_frame:
			    # Find all the faces and face encodings in the current frame of video
			    face_locations = face_recognition.face_locations(rgb_small_frame)
			    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			    face_names = []
			    for face_encoding in face_encodings:
			        # See if the face is a match for the known face(s)
			        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			        name = "Unknown"
			        # # If a match was found in known_face_encodings, just use the first one.
			        # if True in matches:
			        #     first_match_index = matches.index(True)
			        #     name = known_face_names[first_match_index]

			        # Or instead, use the known face with the smallest distance to the new face
			        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			        best_match_index = np.argmin(face_distances)
			        # percent = face_distances[best_match_index]*100
			        # percent = str(100.00 - round(percent,2))
			        # percent = percent[0:5]

			        if matches[best_match_index]:
			            name = known_face_names[best_match_index]
			        else:
			            name = "Unknown"

			        face_names.append(name)
			        for s in studentsInClass:
			        	for f in face_names:
			        		if s == f:
			        			student_id = f.split(":")[1]
			        			student = Student.objects.get(student_id=student_id)
			        			date = datetime.date.today()
			        			classcourse = ClassCourse.objects.get(id=class_id)
			        			check = Attendance.objects.filter(student=student, classcourse=classcourse,
			        				date=date).last()
			        			print(check)
			        			if check == None or check.entry == 'exit':
			        				print(s+' enters the room at: '+ time)
			        				att = Attendance(student=student, classcourse=classcourse, 
			        					date=date, time=time, entry='enter')
			        				att.save()
			        # print('video 1: ',face_id)

			process_this_frame = not process_this_frame

			font = cv2.FONT_HERSHEY_DUPLEX
			# Display the results
			for (top, right, bottom, left), name in zip(face_locations, face_names):
			    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
			    top *= 4
			    right *= 4
			    bottom *= 4
			    left *= 4

			    # Draw a box around the face
			    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
			    name if not name == "Unknown" else "Unknown"
			    # Draw a label with a name below the face
			    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

			# Display the resulting image

			retval, jpeg = cv2.imencode('.jpg', frame)
			return jpeg.tobytes()

class VideoCamera2(object):
	def __init__(self, index=1):
		self.video = cv2.VideoCapture(index)
		print(self.video.isOpened())
	    
	def _del_(self):
		self.video.release()
	    
	def get_frame(self,in_graysale=False):
		# Initialize some variables
		global entrance
		face_locations = []
		face_encodings = []
		
		process_this_frame = True

		known_face_encodings = []
		known_face_names = []

		# query name and face encodings from the database
		enc = Encoding.objects.all()
		for e in enc:
			id = e.id
			encoding = Encoding.objects.get(id=id)
			face = Face.objects.get(encoding=encoding)
			name = Student.objects.get(face=face)
			encodings = base64.b64decode(encoding.encoding)
			encodings = pickle.loads(encodings)
			known_face_encodings.append(encodings)
			known_face_names.append(str(name))

		# check today class
		day = datetime.datetime.today().strftime("%A")
		time = datetime.datetime.today().strftime("%H:%M")
		studentsInClass = []
		class_id = None
		cd = ClassDay.objects.filter(day=day)
		for cd in cd:
			cc = ClassCourse.objects.get(classday=cd)
			start = cc.start
			start = start.strftime("%H:%M")
			end = cc.end
			end = end.strftime("%H:%M")
			# check if a student is detected during this time
			if time >= start and time <= end:
				class_id = cc.id
				se = StudentEnrollClass.objects.filter(classcourse=cc)
				for se in se:
					student = str(se.student)
					studentsInClass.append(student)
				# timeout everyone exit
				if time == end:
					date = datetime.date.today()
					att = Attendance.objects.filter(classcourse=cc,date=date)
					tmp = []
					student_id = int()
					for a in att:
						a = str(a.student)
						student_id= a.split(":")[1]
						student = Student.objects.get(student_id=student_id)
						check = Attendance.objects.filter(student=student)
						for c in check:
							tmp.append(c.entry)
						if tmp[-1] == 'enter':
							student = Student.objects.get(student_id=student_id)
							classcourse = ClassCourse.objects.get(id=class_id)
							exitTime = datetime.datetime.strptime(time,'%H:%M').time()
							att = Attendance(student=student, classcourse=classcourse, 
								date=date, time=exitTime, entry='exit')
							att.save()
							entrance = "Exit"

		while True:
			# Grab a single frame of video
			ret, frame = self.video.read()

			# Resize frame of video to 1/4 size for faster face recognition processing
			small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

			# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
			rgb_small_frame = small_frame[:, :, ::-1]

			# Only process every other frame of video to save time
			if process_this_frame:
			    # Find all the faces and face encodings in the current frame of video
			    face_locations = face_recognition.face_locations(rgb_small_frame)
			    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			    face_names = []
			    for face_encoding in face_encodings:
			        # See if the face is a match for the known face(s)
			        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			        name = "Unknown"
			        # # If a match was found in known_face_encodings, just use the first one.
			        # if True in matches:
			        #     first_match_index = matches.index(True)
			        #     name = known_face_names[first_match_index]

			        # Or instead, use the known face with the smallest distance to the new face
			        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			        best_match_index = np.argmin(face_distances)
			        # percent = face_distances[best_match_index]*100
			        # percent = str(100.00 - round(percent,2))
			        # percent = percent[0:5]

			        if matches[best_match_index]:
			            name = known_face_names[best_match_index]
			        else:
			            name = "Unknown"

			        face_names.append(name)
			        for s in studentsInClass:
			        	for f in face_names:
			        		if s == f:
			        			student_id= f.split(":")[1]
			        			student = Student.objects.get(student_id=student_id)
			        			date = datetime.date.today()
			        			classcourse = ClassCourse.objects.get(id=class_id)
			        			check = Attendance.objects.filter(student=student, classcourse=classcourse, 
			        				date=date).last()
			        			if check.entry == 'enter':
			        				print(s+' exits the room at: '+ time)
			        				att = Attendance(student=student, classcourse=classcourse, 
			        					date=date, time=time, entry='exit')
			        				att.save()
			        				entrance = "Exit"
			        # print('video 2:',face_names)


			process_this_frame = not process_this_frame

			font = cv2.FONT_HERSHEY_DUPLEX
			# Display the results
			for (top, right, bottom, left), name in zip(face_locations, face_names):
			    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
			    top *= 4
			    right *= 4
			    bottom *= 4
			    left *= 4

			    # Draw a box around the face
			    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
			    name if not name == "Unknown" else "Unknown"
			    # Draw a label with a name below the face
			    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

			# Display the resulting image

			retval, jpeg = cv2.imencode('.jpg', frame)
			return jpeg.tobytes()
	
				

