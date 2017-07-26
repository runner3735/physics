from django.contrib import admin

from .models import Course, Room, Demo, Photo, Note, Keyword

admin.site.register(Course)
admin.site.register(Room)
admin.site.register(Demo)
admin.site.register(Photo)
admin.site.register(Note)
admin.site.register(Keyword)
