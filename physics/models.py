
import os

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from PIL import Image
from io import BytesIO

class Course(models.Model):
  text = models.CharField(max_length=8)

  class Meta: 
    ordering = ["text"]

  def get_absolute_url(self):
    return reverse('course-detail', args=[str(self.id)])
  
  def __str__(self):
    return self.text

class Room(models.Model):
  text = models.CharField(max_length=8)

  class Meta: 
    ordering = ["text"]

  def get_absolute_url(self):
    return reverse('room-detail', args=[str(self.id)])
  
  def __str__(self):
    return self.text

class Component(models.Model):
  name = models.CharField(max_length=128, unique=True)

  class Meta: 
    ordering = ["name"]

  def __str__(self):
    return self.name

class Tag(models.Model):
  text = models.CharField(max_length=128, unique=True)

  class Meta: 
    ordering = ["text"]

  def __str__(self):
    return self.text
  
class Note(models.Model):
  text = models.TextField(max_length=2048)
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta: 
    ordering = ["created"]

  def __str__(self):
    return self.text.splitlines()[0]
    
class Demo(models.Model):
  name = models.CharField(max_length=200, unique=True)
  mainphoto = models.IntegerField(blank=True, null=True, editable=False)
  description = models.TextField(max_length=2048, blank=True)
  course = models.ManyToManyField(Course)
  room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
  location = models.CharField(max_length=200, blank=True)
  modified = models.DateTimeField(auto_now=True)
  components = models.ManyToManyField(Component)
  notes = models.ManyToManyField(Note)
  tags = models.ManyToManyField(Tag)

  class Meta: 
    ordering = ["-id"]

  def get_absolute_url(self):
    return reverse('demo-detail', args=[str(self.id)])
        
  def __str__(self):
    return self.index() + ". " + self.name

  def index(self):
    return 'D' + str(self.id).zfill(3)
  
class Photo(models.Model):
  demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
  caption = models.CharField(max_length=200, blank=True, default="")
  imagefile = models.ImageField(upload_to='photos/')
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  thumbnail = models.ImageField(upload_to='thumbs/', editable=False, null=True)
  created = models.DateTimeField(auto_now_add=True)
  notes = models.ManyToManyField(Note)

  class Meta: 
    ordering = ["created"]

  def __str__(self):
    return self.caption

  def save(self, *args, **kwargs):
    super(Photo, self).save(*args, **kwargs)
          
  def make_thumbnail(self):
    self.save()
    try:
      image = Image.open(self.imagefile)
    except:
      return
    image.thumbnail((500,500), Image.ANTIALIAS)
    filename = self.imagefile.name[7:]
    if filename.lower().endswith('.jpg'):
      FTYPE = 'JPEG'
    elif filename.lower().endswith('.gif'):
      FTYPE = 'GIF'
    elif filename.lower().endswith('.png'):
      FTYPE = 'PNG'
    else:
      return
    tempfile = BytesIO()
    image.save(tempfile, FTYPE)
    tempfile.seek(0)
    content = ContentFile(tempfile.read())
    tempfile.close()
    self.thumbnail.save(filename, content, save=False)

  def delete_images(self):
    self.imagefile.delete()
    if self.thumbnail:
      self.thumbnail.delete()
      
  def delete(self, *args, **kwargs):
    self.delete_images()
    super(Photo, self).delete(*args, **kwargs)
    
class Attachment(models.Model):
  demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
  description = models.CharField(max_length=200)
  otherfile = models.FileField(upload_to='attachments/')
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta: 
    ordering = ["created"]

  def __str__(self):
    return self.otherfile.name[12:]



