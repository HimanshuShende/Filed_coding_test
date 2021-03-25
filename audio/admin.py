from django.contrib import admin
from .models import AudioBook, Song, Podcast
# Register your models here.
admin.site.register(AudioBook)
admin.site.register(Song)
admin.site.register(Podcast)