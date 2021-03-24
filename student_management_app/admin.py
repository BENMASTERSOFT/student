from django.contrib import admin
from student_management_app.models import CustomUser, Staffs

from django.contrib.auth.admin import UserAdmin


class UserModel(UserAdmin):
	pass


admin.site.register(CustomUser,UserModel)
admin.site.register(Staffs)
