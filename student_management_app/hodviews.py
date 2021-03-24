from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from student_management_app.models import CustomUser, Courses, Staffs, Subjects, Students, SessionYearModel, \
	FeedBackStudent, FeedBackStaffs, LeaveReportStudent,LeaveReportStaff, Attendance, AttendanceReport
from django.contrib import messages
from django.urls import reverse
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import AddStudentForm, EditStudentForm
from django.views.decorators.csrf import csrf_exempt
import json



def admin_home(request):
	students_count=Students.objects.all().count()
	staff_count=Staffs.objects.all().count()
	subjects_count=Subjects.objects.all().count()
	course_count=Courses.objects.all().count()

	course_all=Courses.objects.all()
	course_name_list=[]
	subject_count_list=[]
	student_count_list_in_course=[]

	for course in course_all:
		subjects=Subjects.objects.filter(course_id=course.id).count()
		students=Students.objects.filter(course_id=course.id).count()
		course_name_list.append(course.course_name)
		subject_count_list.append(subjects)
		student_count_list_in_course.append(students)

	subjects_all=Subjects.objects.all()
	subject_list=[]
	student_count_list_in_subject=[]
	for subject in subjects_all:
		course=Courses.objects.get(id=subject.course_id.id)
		student_count=Students.objects.filter(course_id=course.id).count()
		subject_list.append(subject.subject_name)
		student_count_list_in_subject.append(student_count)


	staffs=Staffs.objects.all()
	attendance_present_list_staff=[]
	attendance_absent_list_staff=[]
	staff_name_list=[]
	for staff in staffs:
		subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
		attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
		leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
		attendance_present_list_staff.append(attendance)
		attendance_absent_list_staff.append(leaves)
		staff_name_list.append(staff.admin.username)



	students_all=Students.objects.all()
	attendance_present_list_student=[]
	attendance_absent_list_student=[]
	student_name_list=[]
	for student in students_all:
		attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
		absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
		leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
		attendance_present_list_student.append(attendance)
		attendance_absent_list_student.append(absent)
		student_name_list.append(student.admin.username)


	context={
		'student_name_list':student_name_list,
		'attendance_present_list_student':attendance_present_list_student,
		'attendance_absent_list_student':attendance_absent_list_student,
		'staff_name_list':staff_name_list,
		'attendance_present_list_staff':attendance_present_list_staff,
		'attendance_absent_list_staff':attendance_absent_list_staff,
		'student_count_list_in_subject':student_count_list_in_subject,
		'subject_list':subject_list,
		'subject_count_list':subject_count_list,
		'course_name_list':course_name_list,
		'students_count':students_count,
		'staff_count':staff_count,
		'subjects_count':subjects_count,
		'course_count':course_count,
		'student_count_list_in_course':student_count_list_in_course,
		}
	return render(request, "hod_templates/home_content.html",context)


def add_staff(request):
	return render(request, "hod_templates/add_staff_template.html")


def add_staff_save(request):
	if request.method != "POST":
		return HttpResponse("Method Not Allowed")
	else:
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		username = request.POST.get("username")
		email = request.POST.get("email")
		password= request.POST.get("password")
		address= request.POST.get("address")
		try:
			user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
			user.staffs.address=address
			user.save()
			messages.success(request,"Staff Added Successfully")
			return HttpResponseRedirect(reverse("add_staff"))
		except:
			messages.error(request,"Failed to add Staff")
			return HttpResponseRedirect(reverse("add_staff")) 


def add_course(request):
	return render(request, "hod_templates/add_course_template.html")


def add_course_save(request):
	if request.method != "POST":
		return HttpResponseRedirect("Method Not Allowed")
	else:
		course=request.POST.get("course")
		print(course)
		try:
			course_model = Courses(course_name=course)
			course_model.save()
			messages.success(request,"Course Added Successfully")
			return HttpResponseRedirect(reverse("add_course"))
		except:
			messages.error(request,"Failed to Add Course")
			return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
	# courses = Courses.objects.all()
	form = AddStudentForm()
	context={
	
	'form':form,

	}
	return render(request, "hod_templates/add_student_template.html", context)


def add_student_save(request):
	if request.method != "POST":
		return HttpResponse("Method Not Allowed")
	else:
		form=AddStudentForm(request.POST,request.FILES)
		if form.is_valid():
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password= form.cleaned_data["password"]
			address= form.cleaned_data["address"]
			course_id = form.cleaned_data["course"]
			sex= form.cleaned_data["sex"]
			session_year_id= form.cleaned_data["session_year_id"]
			

			if request.FILES.get('profile_pic', False):
				profile_pic = request.FILES['profile_pic']
				fs=FileSystemStorage()
				filename=fs.save(profile_pic.name,profile_pic)
				profile_pic_url=fs.url(filename)
			else:
				profile_pic_url=None


			try:
				user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
				user.students.address=address
				user.students.gender=sex
				course_obj = Courses.objects.get(pk=course_id)
				user.students.course_id=course_obj 
				session_year=SessionYearModel.objects.get(id=session_year_id)
				user.students.session_year_id=session_year
			
				if profile_pic_url!=None:
					user.students.profile_pic=profile_pic_url

				user.save()
				messages.success(request,"Student Added Successfully")
				return HttpResponseRedirect(reverse("add_student"))
			except:
				messages.error(request,"Failed to add Student")
				return HttpResponseRedirect(reverse("add_student")) 
		else:
			form = AddStudentForm(request.POST)	
			return render(request, "hod_templates/add_student_template.html", {'form':form})	



def add_subject(request):
	courses = Courses.objects.all()
	staffs = CustomUser.objects.filter(user_type=2)
	context ={
	'courses':courses,
	'staffs':staffs,
	}
	return render(request, "hod_templates/add_subject_template.html", context)



def add_subject_save(request):
	if request.method != "POST":
		return HttpResponse("<h2>Method Not Allowed</h2>")
	else:
		subject_name = request.POST.get("subject_name")
		course_id = request.POST.get("course")
		course = Courses.objects.get(pk=course_id)
		staff_id = request.POST.get("staff")
		staff=CustomUser.objects.get(id=staff_id)
		
		try:
			subject = Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
			subject.save()
			messages.success(request,"Subject Added Successfully")
			return HttpResponseRedirect(reverse("add_subject"))
		except:
			messages.error(request,"Failed to add Subject")
			return HttpResponseRedirect(reverse("add_subject")) 


def manage_staff(request):
	staffs = Staffs.objects.all()
	return render(request, "hod_templates/manage_staff_template.html",{'staffs':staffs})


def manage_student(request):
	students = Students.objects.all()
	
	return render(request, "hod_templates/manage_student_template.html",{'students':students})


def manage_course(request):
	courses = Courses.objects.all()
	return render(request, "hod_templates/manage_course_template.html",{'courses':courses})


def manage_subject(request):
	subjects = Subjects.objects.all()
	return render(request, "hod_templates/manage_subject_template.html",{'subjects':subjects})



def edit_staff(request, staff_id):
	staff = Staffs.objects.get(admin=staff_id)	
	return render(request, "hod_templates/edit_staff_template.html",{'staff':staff, 'id':staff_id})

def edit_staff_save(request):
	if request.method!="POST":
		return HttpResponse("Method Not Allowed")
	else: 
		staff_id = request.POST.get("staff_id")
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		email = request.POST.get("email")
		username = request.POST.get("username")
		address = request.POST.get("address")
		try:
			user = CustomUser.objects.get(id=staff_id)
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.username = username
			user.save()

			staff_model = Staffs.objects.get(admin=staff_id)
			staff_model.address = address
			staff_model.save()
			messages.success(request,"Staff Edited Successfully")
			return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
		except:
			messages.error(request,"Failed to edit Staff")
			return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

			
def edit_student(request, student_id):
	request.session['student_id']=student_id
	student = Students.objects.get(admin=student_id)
	form=EditStudentForm()
	form.fields['email'].initial=student.admin.email
	form.fields['first_name'].initial=student.admin.first_name
	form.fields['last_name'].initial=student.admin.last_name
	form.fields['username'].initial=student.admin.username
	username=student.admin.username
	form.fields['address'].initial=student.address
	form.fields['course'].initial=student.course_id.id
	form.fields['sex'].initial=student.gender
	form.fields['session_year_id'].initial=student.session_year_id

	# session_year_id= form.cleaned_data["session_year_id"]
	return render(request, "hod_templates/edit_student_template.html",{'form':form,"id":student_id,"username":username})


def edit_student_save(request):
	if request.method!="POST":
		return HttpResponse("Method Not Allowed")
	else: 
		student_id=request.session.get("student_id")
		if student_id==None:
			return HttpResponseRedirect(reverse("manage_student"))

		form=EditStudentForm(request.POST,request.FILES)
		if form.is_valid():
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			address = form.cleaned_data["address"]
			session_year_id= form.cleaned_data["session_year_id"]
			course_id = form.cleaned_data["course"]
			sex = form.cleaned_data["sex"]

			if request.FILES.get('profile_pic', False):
				profile_pic = request.FILES['profile_pic']
				fs=FileSystemStorage()
				filename=fs.save(profile_pic.name,profile_pic)
				profile_pic_url=fs.url(filename)
			else:
				profile_pic_url=None

			try:
				user = CustomUser.objects.get(id=student_id)
				user.first_name = first_name
				user.last_name = last_name
				user.username = username
				user.email = email
				user.save()

				student = Students.objects.get(admin=student_id)		
				student.address = address
				session_year=SessionYearModel.objects.get(id=session_year_id)
				student.session_year_id=session_year
				student.gender = sex
				if profile_pic_url!=None:
					student.profile_pic=profile_pic_url
			
				course = Courses.objects.get(id=course_id)
				
				student.course_id = course
				student.save()

				del request.session['student_id']
				messages.success(request,"student Edited Successfully")
				return HttpResponseRedirect(reverse('edit_student',kwargs={"student_id":student_id}))
			except:
				messages.error(request,"Failed to edit student")
				return HttpResponseRedirect(reverse('edit_student',kwargs={"student_id":student_id}))
		else:
			form = EditStudentForm(request.POST)
			student=Students.objects.get(admin=student_id)	
			return render(request, "hod_templates/edit_student_template.html", {'form':form,'id':student_id,'username':student.admin.username})



def edit_course(request,course_id):
	course = Courses.objects.get(id=course_id)	
	return render(request, "hod_templates/edit_course_template.html",{'course':course,"id":course_id})


def edit_course_save(request):
	if request.method!="POST":
		return HttpResponse("Method Not Allowed")
	else: 
		course_id = request.POST.get("course_id")
		course_name = request.POST.get("course")
	

		try:
			course = Courses.objects.get(id=course_id)
			course.course_name = course_name
			course.save()

			messages.success(request,"Course Edited Successfully")
			return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
		except:
			messages.error(request,"Failed to edit course")
			return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def edit_subject(request,subject_id):
	subject = Subjects.objects.get(id=subject_id)
	courses = Courses.objects.all()
	staffs = CustomUser.objects.filter(user_type=2)
	context ={
	'courses':courses,
	'staffs':staffs,
	'subject':subject,
	"id":subject_id,
	}	
	return render(request, "hod_templates/edit_subject_template.html",context)


def edit_subject_save(request):
	if request.method!="POST":
		return HttpResponse("Method Not Allowed")
	else: 
		subject_id = request.POST.get("subject_id")
		subject_name = request.POST.get("subject_name")
		
		course_id = request.POST.get("course")
		staff_id = request.POST.get("staff")
	
		try:
			subject = Subjects.objects.get(id=subject_id)
			subject.subject_name=subject_name

			staff=CustomUser.objects.get(id=staff_id)
			subject.staff_id = staff

			course=Courses.objects.get(id=course_id)
			subject.course_id = course
			subject.save()

			messages.success(request,"Subject Edited Successfully")
			return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
		except:
			messages.error(request,"Failed to edit subject")
			return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def manage_session(request):
	return render(request,"hod_templates/manage_session_template.html")


def add_session_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse("manage_session"))
	else: 
		session_start_year = request.POST.get("session_start")
		session_end_year = request.POST.get("session_end")
		
		try:
			session = SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
			
			session.save()
			messages.success(request,"Session Added Successfully")
			return HttpResponseRedirect(reverse("manage_session"))
		except:
			messages.error(request,"Failed to add Session")
			return HttpResponseRedirect(reverse("manage_session")) 


@csrf_exempt
def check_email_exist(request):
	email=request.POST.get("email")
	user_obj=CustomUser.objects.filter(email=email).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return  HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
	username=request.POST.get("username")
	user_obj=CustomUser.objects.filter(username=username).exists()
	if user_obj:
		return HttpResponse(True)
	else:
		return  HttpResponse(False)


def student_feedback_message(request):
	feedbacks=FeedBackStudent.objects.all()
	context={
	'feedbacks':feedbacks,
	}
	return render(request, 'hod_templates/student_feedback_template.html', context)


def staff_feedback_message(request):
	feedbacks=FeedBackStaffs.objects.all()
	context={
	'feedbacks':feedbacks,
	}
	return render(request, 'hod_templates/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_replied(request):
	feedback_id=request.POST.get("id")
	feedback_message=request.POST.get("message")

	try:
		feedback=FeedBackStaffs.objects.get(id=feedback_id)
		feedback.feedback_reply=feedback_message
		feedback.save()
		return HttpResponse("True")
	except:
		return HttpResponse("False")


@csrf_exempt
def student_feedback_message_replied(request):
	feedback_id=request.POST.get("id")
	feedback_message=request.POST.get("message")

	try:
		feedback=FeedBackStudent.objects.get(id=feedback_id)
		feedback.feedback_reply=feedback_message
		feedback.save()
		return HttpResponse("True")
	except:
		return HttpResponse("False")


def staff_leave_view(request):
	leaves = LeaveReportStaff.objects.all()
	return render(request,'hod_templates/staff_leave_view.html',{'leaves':leaves})

def staff_approve_leave(request, leave_id):
	leave=LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status=1
	leave.save()
	return HttpResponseRedirect(reverse('staff_leave_view')) 


def staff_disapprove_leave(request, leave_id):
	leave=LeaveReportStaff.objects.get(id=leave_id)
	leave.leave_status=2
	leave.save()
	return HttpResponseRedirect(reverse('staff_leave_view')) 




def student_leave_view(request):
	leaves = LeaveReportStudent.objects.all()
	return render(request,'hod_templates/student_leave_view.html',{'leaves':leaves})


def student_approve_leave(request, leave_id):
	leave=LeaveReportStudent.objects.get(id=leave_id)
	leave.leave_status=1
	leave.save()
	return HttpResponseRedirect(reverse('student_leave_view')) 


def student_disapprove_leave(request, leave_id):
	leave=LeaveReportStudent.objects.get(id=leave_id)
	leave.leave_status=2
	leave.save()
	return HttpResponseRedirect(reverse('student_leave_view')) 	



def admin_view_attendance(request):
	subjects = Subjects.objects.all()
	session_year_id=SessionYearModel.objects.all()
	context ={
	'subjects':subjects,
	'session_year_id':session_year_id,
	}
	return render(request,'hod_templates/admin_view_attendance.html',context)


@csrf_exempt
def admin_get_attendancd_dates(request):
	subject=request.POST.get("subject")
	session_year_id=request.POST.get("session_year_id")

	subject_obj=Subjects.objects.get(id=subject)
	session_year_obj=SessionYearModel.objects.get(id=session_year_id)
	
	attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)

	attendance_obj = []
	for attendance_single in attendance:
		data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
		attendance_obj.append(data)

	return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
	attendance_date = request.POST.get("attendance_date")	
	attendance=Attendance.objects.get(id=attendance_date)

	attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)

	list_data=[]

	for student in attendance_data:
		data_small = {'id':student.student_id.admin.id,'name':student.student_id.admin.first_name + " " +student.student_id.admin.last_name,"status":student.status}
		list_data.append(data_small)
	return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



def admin_profile(request):
	user=CustomUser.objects.get(id=request.user.id)
	return render(request,"hod_templates/admin_profile.html",{'user':user}) 


def edit_profile_save(request):
	if request.method!="POST":
		return HttpResponseRedirect(reverse("admin_profile"))
	else:
		first_name=request.POST.get("first_name")
		last_name=request.POST.get("last_name")
		password=request.POST.get("password")

		try:
			customuser=CustomUser.objects.get(id=request.user.id)
			customuser.first_name=first_name
			customuser.last_name=last_name
			if password!=None and password!="":
				customuser.set_password(password)
			customuser.save()
			messages.success(request, "Successfully Updated Profile")
			return HttpResponseRedirect(reverse("admin_profile"))
		except:
			messages.error(request, "Failed to Updated Profile")
			return HttpResponseRedirect(reverse("admin_profile"))
