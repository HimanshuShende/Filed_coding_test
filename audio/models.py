from django.db import models

class Song(models.Model):
    class Meta:
        verbose_name = "Song"
        verbose_name_plural = "Songs"
    name = models.CharField(verbose_name="Name",max_length = 100)
    duration = models.IntegerField(verbose_name="Duration")
    uploaded_time = models.DateTimeField(auto_now=True, verbose_name="Uploaded time")
        
class Podcast(models.Model):
    class Meta:
        verbose_name = "Podcast"
        verbose_name_plural = "Podcasts"
    name = models.CharField(verbose_name="Name",max_length = 100)
    host = models.CharField(verbose_name="Host",max_length = 100)
    participants = models.TextField(verbose_name="Participants",null=True, blank=True)
    duration = models.IntegerField(verbose_name="Duration")
    uploaded_time = models.DateTimeField(auto_now=True, verbose_name="Uploaded time")

class AudioBook(models.Model):
    class Meta:
        verbose_name = "Audio Book"
        verbose_name_plural = "Audio Books"
    title = models.CharField(verbose_name="Title",max_length = 100)
    author = models.CharField(verbose_name="Author",max_length = 100)
    narrator = models.CharField(verbose_name="Narrator",max_length = 100)
    duration = models.IntegerField(verbose_name="Duration")
    uploaded_time = models.DateTimeField(auto_now=True, verbose_name="Uploaded time")
    
    
    
        