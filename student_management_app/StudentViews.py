import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import SessionYearModel, Students, Courses, Subjects, CustomUser, Attendance,AttendanceReport, FeedBackStudent, \
	LeaveReportStudent


def student_home(request):
	student_obj=Students.objects.get(admin=request.user.id)
	attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
	attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
	attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
	course=Courses.objects.get(id=student_obj.course_id.id)
	subjects=Subjects.objects.filter(course_id=course).count()

	
	subject_name=[]
	data_present=[]
	data_absent=[]
	subject_data=Subjects.objects.filter(course_id=student_obj.course_id)

	for subject in subject_data:
		attendance=Attendance.objects.filter(subject_id=subject.id)
		attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
		attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
		subject_name.append(subject.subject_name)
		data_present.append(attendance_present_count)
		data_absent.append(attendance_absent_count)

	context={
	'data_name':subject_name,
	'data1':data_present,
	'data2':data_absent,
	'attendance_total':attendance_total,
	'attendance_present':attendance_present,
	'attendance_absent':attendance_absent,
	'subjects':subjects,
	}
	return render(request, "student_template/student_home_template.html",context)


def student_view_attendance(request):
	student=Students.objects.get(admin=request.user.id)
	course = student.course_id.id
	subjects=Subjects.objects.filter(course_id=course)
	session_years=SessionYearModel.objects.all()

	context ={
	'student':student,
	'course':course,
	'subjects' : subjects,
	'session_years' : session_years,
	}
	return render(request,'student_template/student_view_attendance.html',context)


def student_view_attendance_post(request):
	subject_id=request.POST.get("subject")
	start_date=request.POST.get("start_date")
	end_date=request.POST.get("end_date")

	start_data_parse=datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
	end_data_parse=datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
	subject_obj=Subjects.objects.get(id=subject_id)
	user_object=CustomUser.objects.get(id=request.user.id)
	stud_obj=Students.objects.get(admin=user_object)

	attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
	attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
	context={
	'attendance_reports':attendance_reports,
	}
	return render(request,'student_template/student_attendance_data.html',context)


def student_apply_leave(request):
	student_obj=Students.objects.get(admin=request.user.id)
	leave_data=LeaveReportStudent.objects.filter(student_id=student_obj)
	return render(request, 'student_template/student_apply_leave.html',{'leave_data':leave_data})
	

	


def student_apply_leave_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse("student_apply_leave"))
	else:
		leave_date=request.POST.get("leave_date")
		leave_msg=request.POST.get("leave_msg")

		student_obj=Students.objects.get(admin=request.user.id)

		try:
			leave_report=LeaveReportStudent(student_id=student_obj, leave_date=leave_date,leave_message=leave_msg,leave_status=0)
			leave_report.save()
			messages.success(request,"Leave Added Successfully")
			return HttpResponseRedirect(reverse("student_apply_leave"))
		except:
			messages.error(request,"Failed to add Student Leave")
			return HttpResponseRedirect(reverse("student_apply_leave")) 



def student_feedback(request):
	student_obj=Students.objects.get(admin=request.user.id)
	feedback_data=FeedBackStudent.objects.filter(student_id=student_obj)
	return render(request, 'student_template/student_feedback.html',{'feedback_data':feedback_data})



def student_feedback_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse("student_feedback"))
	else:
		feedback_msg=request.POST.get("feedback_msg")
		

		student_obj=Students.objects.get(admin=request.user.id)

		try:
			feedback=FeedBackStudent(student_id=student_obj, feedback=feedback_msg,feedback_reply="")
			feedback.save()
			messages.success(request,"Feedback Added Successfully")
			return HttpResponseRedirect(reverse("student_feedback"))
		except:
			messages.error(request,"Failed to add Feedback")
			return HttpResponseRedirect(reverse("student_feedback")) 

def student_profile(request):
	user=CustomUser.objects.get(id=request.user.id)
	student=Students.objects.get(admin=user)
	return render(request,"student_template/student_profile.html",{'user':user,"student":student}) 


def student_profile_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse("student_profile"))
	else:
		first_name=request.POST.get("first_name")
		last_name=request.POST.get("last_name")
		address=request.POST.get("address")
		password=request.POST.get("password")

		try:
			customuser=CustomUser.objects.get(id=request.user.id)
			customuser.first_name=first_name
			customuser.last_name=last_name
			if password!=None and password!="":
				customuser.set_password(password)
			customuser.save()

			student=Students.objects.get(admin=customuser.id)
			student.address=address
			student.save()


			messages.success(request, "Successfully Updated Profile")
			return HttpResponseRedirect(reverse("student_profile"))
		except:
			messages.error(request, "Failed to Updated Profile")
			return HttpResponseRedirect(reverse("student_profile"))