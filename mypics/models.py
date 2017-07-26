from django.db import models

class Photo(models.Model):
  caption = models.CharField(max_length=200)
  imagefile = models.ImageField(upload_to='photos/')

  def __str__(self):
    return self.caption
