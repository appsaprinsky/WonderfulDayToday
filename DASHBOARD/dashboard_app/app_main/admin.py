from django.contrib import admin
from .models import ToDo, Profile
from .models import Spendings, UploadFile

admin.site.register(ToDo)
admin.site.register(Profile)
admin.site.register(UploadFile)

admin.site.register(Spendings)

# Register your models here.
