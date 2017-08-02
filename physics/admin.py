from django.contrib import admin

from .models import Course, Room, Demo, Photo, Note

admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Demo)
admin.site.register(Photo)
admin.site.register(Note)
