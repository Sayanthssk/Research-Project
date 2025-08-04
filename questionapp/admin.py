from django.contrib import admin

from questionapp.models import *

# Register your models here.

admin.site.register(Login)
admin.site.register(User_Model)
admin.site.register(Instructions_Model)
admin.site.register(SpontaniousQuestion)
admin.site.register(SpontaniousResult)
admin.site.register(PostQuestion)
admin.site.register(PostResult)
admin.site.register(DemoQuestion)