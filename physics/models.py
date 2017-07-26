
import os

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
#from django.core.files.storage import default_storage as storage

from PIL import Image
#from cStringIO import StringIO
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

class Demo(models.Model):
  name = models.CharField(max_length=200)
  mainphoto = models.IntegerField(blank=True, null=True, editable=False)
  description = models.TextField(max_length=2048, blank=True)
  course = models.ManyToManyField(Course)
  room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
  location = models.CharField(max_length=200, blank=True)

  class Meta: 
    ordering = ["-id"]

  def get_absolute_url(self):
    return reverse('demo-detail', args=[str(self.id)])
        
  def __str__(self):
    return self.name

  def index(self):
    return 'D' + str(self.id).zfill(3)
  
class Photo(models.Model):
  demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
  caption = models.CharField(max_length=200)
  imagefile = models.ImageField(upload_to='photos/')
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  thumbnail = models.ImageField(upload_to='thumbs/', editable=False, null=True)

  class Meta: 
    ordering = ["id"]

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

  class Meta: 
    ordering = ["id"]

  def __str__(self):
    return self.otherfile.name[12:]
  
class Note(models.Model):
  demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
  text = models.TextField(max_length=2048)
  contributor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

  class Meta: 
    ordering = ["id"]

  def __str__(self):
    if self.contributor:
      return self.contributor.get_username() + ": " + self.text[:45] + "..."
    else:
      return self.text[:45] + "..."

class Keyword(models.Model):
  demo = models.ForeignKey(Demo, on_delete=models.CASCADE)
  text = models.CharField(max_length=128)

  class Meta: 
    ordering = ["text"]

  def __str__(self):
    return self.text
