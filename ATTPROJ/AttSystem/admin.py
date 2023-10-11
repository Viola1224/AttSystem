from django.contrib import admin
from django.contrib.auth.models import User

from AttSystem import models
# Register your models here.

class ProfileInLine(admin.StackedInline):
    model = models.UserProfile
    #Inline和ModelAdmin类的作用在于，可以在Model A(USER)页面上编辑Model B(USERPROFILE)表的字段，
    # A和B存在外键关系即可。

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInLine,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.Class)
admin.site.register(models.Student)
admin.site.register(models.Semester)
admin.site.register(models.College_Day)
admin.site.register(models.Lecturer)
admin.site.register(models.Course)





