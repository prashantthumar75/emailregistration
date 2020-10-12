# from django.contrib import admin
# from .models import *
# # Register your models here.
#
#
# @admin.register(Teachermodel12)
# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ['teh']
#
#
# @admin.register(ClassesModel)
# class ClassAdmin(admin.ModelAdmin):
#     list_display = ['Class','admist']
#
#
# @admin.register(AdminstrModel)
# class AdminstrAdmin(admin.ModelAdmin):
#     list_display = ['name']
#
#
# @admin.register(DivModel)
# class DivAdmin(admin.ModelAdmin):
#     list_display = ['nameDiv','teachers']
#



from django.contrib import admin

from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'email', 'is_active', 'has_email_verified', )

    def email(self, profile):
        return profile.user.email

    def name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name

    def is_active(self, profile):
        return profile.user.is_active

    def team(self, profile):
        return profile.user.team


# @admin.register(CustomUser)
# class CustomUseAdmin(admin.ModelAdmin):
#     list_display = ['username','password','phone_num']