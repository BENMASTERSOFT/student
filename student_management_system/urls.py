from django.contrib import admin
from django.urls import path, include
from student_management_system import settings
from django.conf.urls.static import static
from student_management_app import views, hodviews, StaffViews, StudentViews
from django.views.generic import TemplateView



urlpatterns = [
    # General Url Path
    path('demo/', views.ShowDemoPage),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin', views.doLogin, name="do_login"),

     # HOD Url Path
    path('admin_home',hodviews.admin_home, name="admin_home"),
    path('add_staff',hodviews.add_staff, name="add_staff"),
    path('add_staff_save',hodviews.add_staff_save,name="add_staff_save"),
    path('add_course',hodviews.add_course,name="add_course"),
    path('add_course_save',hodviews.add_course_save,name="add_course_save"),
    path('add_student',hodviews.add_student, name="add_student"),
    path('add_student_save',hodviews.add_student_save,name="add_student_save"),
    path('add_subject',hodviews.add_subject, name="add_subject"),
    path('add_subject_save',hodviews.add_subject_save,name="add_subject_save"),
    path('manage_staff',hodviews.manage_staff,name="manage_staff"),
    path('manage_student',hodviews.manage_student,name="manage_student"),
    path('manage_course',hodviews.manage_course,name="manage_course"),
    path('manage_subject',hodviews.manage_subject,name="manage_subject"), 
    path('edit_staff/<str:staff_id>',hodviews.edit_staff,name="edit_staff"), 
    path('edit_staff_save',hodviews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', hodviews.edit_student,name="edit_student"), 
    path('edit_student_save', hodviews.edit_student_save,name="edit_student_save"),
    path('edit_course/<str:course_id>', hodviews.edit_course,name="edit_course"), 
    path('edit_course_save', hodviews.edit_course_save,name="edit_course_save"),
    path('edit_subject/<str:subject_id>', hodviews.edit_subject,name="edit_subject"), 
    path('edit_subject_save', hodviews.edit_subject_save,name="edit_subject_save"),
    path('manage_session', hodviews.manage_session,name="manage_session"),
    path('add_session_save', hodviews.add_session_save,name="add_session_save"),
    path('check_email_exist', hodviews.check_email_exist,name="check_email_exist"),
    path('check_username_exist', hodviews.check_username_exist,name="check_username_exist"),
    path('student_feedback_message', hodviews.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replied', hodviews.student_feedback_message_replied,name="student_feedback_message_replied"),
    path('staff_feedback_message', hodviews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replied', hodviews.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('student_leave_view', hodviews.student_leave_view,name="student_leave_view"),
    path('admin_get_attendance_student', hodviews.admin_get_attendance_student,name="admin_get_attendance_student"),
    path('admin_profile', hodviews.admin_profile,name="admin_profile"),
    path('edit_profile_save', hodviews.edit_profile_save,name="edit_profile_save"),
    

    path('staff_leave_view', hodviews.staff_leave_view,name="staff_leave_view"),
    path('student_approve_leave/<str:leave_id>', hodviews.student_approve_leave,name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', hodviews.student_disapprove_leave,name="student_disapprove_leave"),
    path('staff_approve_leave/<str:leave_id>', hodviews.staff_approve_leave,name="staff_approve_leave"),
    path('staff_disapprove_leave/<str:leave_id>', hodviews.staff_disapprove_leave,name="staff_disapprove_leave"),
    path('admin_view_attendance', hodviews.admin_view_attendance,name="admin_view_attendance"),
    path('admin_get_attendancd_dates', hodviews.admin_get_attendancd_dates,name="admin_get_attendancd_dates"),



    # Staff Url Path
    path('staff_home',StaffViews.staff_home, name="staff_home"),   
    path('staff_take_attendance',StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance',StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students',StaffViews.get_students, name="get_students"),
    path('get_attendancd_dates',StaffViews.get_attendancd_dates, name="get_attendancd_dates"),
    path('get_attendance_student',StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data',StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data',StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave',StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save',StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback',StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save',StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile', StaffViews.staff_profile,name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save,name="staff_profile_save"),


    # Student Url Path
    path('student_home',StudentViews.student_home, name="student_home"),
    path('student_view_attendance',StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post',StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave',StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save',StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback',StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save',StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile,name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save,name="student_profile_save"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
