from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Photo

def index(request):
  allpics = Photo.objects.all()
  context = { 'allpics': allpics }
  return render(request, 'mypics/index.htm', context)

def detail(request, pk):
  pic = get_object_or_404(Photo, id=pk)
  return render(request, 'mypics/detail.htm', {'pic': pic})
