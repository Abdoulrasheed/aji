from django.contrib.auth.models import Group
from django.contrib import admin
from app.models import  Gate

admin.site.unregister(Group)
admin.site.register(Gate)

admin.site.site_header = 'Jimeta Ultra Modern Market Administrator'
admin.site.site_title = 'Jimeta Ultra Modern Market'