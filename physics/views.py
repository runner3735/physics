
import os, subprocess

from django.conf import settings
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.db.models import F

from .models import Course, Demo, Photo, Room, Note, Attachment, Component, Tag
from .forms import NameForm, DescriptionForm, CourseForm, RoomForm, LocationForm, DemoForm, NoteForm, TagForm
from .forms import NewPhotoForm, UpdatePhotoForm, NewFileForm, UpdateFileForm

def index(request):
  num_demos = Demo.objects.all().count()
  num_photos = Photo.objects.all().count()
  return render(request, 'index.html', context={'num_demos':num_demos,'num_photos':num_photos})

class DemoCreate(LoginRequiredMixin, CreateView):
  model = Demo
  form_class = DemoForm
  
class DemoListView(generic.ListView):
  model = Demo
  paginate_by = 20

def demos_by_tag(request, tag):
  tags = Tag.objects.all()
  return render(request, 'physics/demos_by_tag.html', {'tags': tags})

class DemoDetailView(generic.DetailView):
  model = Demo
    
class CourseListView(generic.ListView):
  model = Course

class CourseDetailView(generic.DetailView):
  model = Course
    
class RoomListView(generic.ListView):
  model = Room

class RoomDetailView(generic.DetailView):
  model = Room

class MyPhotosListView(LoginRequiredMixin,generic.ListView):
    model = Photo
    template_name ='physics/my_photo_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Photo.objects.filter(contributor=self.request.user)

class DemoPhotoView(generic.ListView):
    model = Photo
    template_name ='physics/main_photo_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Photo.objects.filter(demo__mainphoto=F('id'))
      
@login_required
def name_update(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NameForm(request.POST)
    if form.is_valid():
      demo.name = form.cleaned_data['name']
      demo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = NameForm(initial={'name': demo.name})
  return render(request, 'physics/name_update.html', {'form': form, 'demo': demo})

@login_required
def course_update(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = CourseForm(request.POST)
    if form.is_valid():
      demo.course = form.cleaned_data['course']
      demo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = CourseForm(initial={'course': demo.course.all})
  return render(request, 'physics/course_update.html', {'form': form, 'demo': demo})

@login_required
def room_update(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      demo.room = form.cleaned_data['room']
      demo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = RoomForm(initial={'room': demo.room})
  return render(request, 'physics/room_update.html', {'form': form, 'demo': demo})

@login_required
def location_update(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = LocationForm(request.POST)
    if form.is_valid():
      demo.location = form.cleaned_data['location']
      demo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = LocationForm(initial={'location': demo.location})
  return render(request, 'physics/location_update.html', {'form': form, 'demo': demo})

@login_required
def description_update(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = DescriptionForm(request.POST)
    if form.is_valid():
      demo.description = form.cleaned_data['description']
      demo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = DescriptionForm(initial={'description': demo.description})
  return render(request, 'physics/description_update.html', {'form': form, 'demo': demo})

# Photo

def photo_detail(request, pk):
  photo = get_object_or_404(Photo, pk = pk)
  return render(request, 'physics/photo_detail.html', {'photo': photo})

@login_required
def add_photo(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NewPhotoForm(request.POST, request.FILES)
    if form.is_valid():
      photo = Photo()
      photo.demo = demo
      photo.caption = form.cleaned_data['caption']
      photo.imagefile = form.cleaned_data['imagefile']
      photo.contributor = request.user
      photo.make_thumbnail()
      photo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))
  else:
    form = NewPhotoForm()
  return render(request, 'physics/new_photo.html', {'form': form, 'demo': demo})

@login_required
def update_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  if request.user != photo.contributor:
    return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))
  elif request.method == 'POST':
    form = UpdatePhotoForm(request.POST, request.FILES)
    if form.is_valid():
      photo.caption = form.cleaned_data['caption']
      if form.cleaned_data['imagefile']:
        photo.delete_images()
        photo.imagefile = form.cleaned_data['imagefile']
        photo.make_thumbnail()
      photo.save()
      return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))
  else:
    form = UpdatePhotoForm(initial={'caption': photo.caption})
  return render(request, 'physics/update_photo.html', {'form': form, 'photo': photo})

@login_required
def delete_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  demo = photo.demo
  if photo.contributor == request.user:
    photo.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))

@login_required
def main_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  photo.demo.mainphoto = pk
  photo.demo.save()
  return HttpResponseRedirect(reverse('demo-detail', args=[photo.demo.id]))

# Attachment

@login_required
def add_file(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NewFileForm(request.POST, request.FILES)
    if form.is_valid():
      attachment = Attachment()
      attachment.demo = demo
      attachment.otherfile = form.cleaned_data['otherfile']
      attachment.description = form.cleaned_data['description']
      if not attachment.description:
        attachment.description = os.path.basename(attachment.otherfile.name)
      attachment.contributor = request.user
      attachment.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = NewFileForm()
  return render(request, 'physics/new_file.html', {'form': form, 'demo': demo})

@login_required
def update_file(request, pk):
  attachment=get_object_or_404(Attachment, pk = pk)
  if request.user != attachment.contributor:
    return HttpResponseRedirect(reverse('demo-detail', args=[attachment.demo.id]))
  elif request.method == 'POST':
    form = UpdateFileForm(request.POST, request.FILES)
    if form.is_valid():
      attachment.description = form.cleaned_data['description']
      if form.cleaned_data['otherfile']:
        attachment.otherfile.delete()
        attachment.otherfile = form.cleaned_data['otherfile']
      if not attachment.description:
        attachment.description = os.path.basename(attachment.otherfile.name)
      attachment.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[attachment.demo.id]))
  else:
    form = UpdateFileForm(initial={'description': attachment.description})
  return render(request, 'physics/update_file.html', {'form': form, 'attachment': attachment})

@login_required
def delete_file(request, pk):
  attachment=get_object_or_404(Attachment, pk = pk)
  demo = attachment.demo
  if attachment.contributor == request.user:
    attachment.otherfile.delete()
    attachment.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))

@login_required
def convert_file(request, pk):
  attachment=get_object_or_404(Attachment, pk = pk)
  pdfpath = os.path.join(settings.MEDIA_ROOT, attachment.otherfile.name)
  if pdfpath.lower().endswith('.pdf'):
    jpgpath = pdfpath[:-4] + '.jpg'
    if not os.path.exists(jpgpath):
      if convert_pdf(pdfpath, jpgpath):
        photo = Photo()
        photo.demo = attachment.demo
        photo.caption = os.path.basename(jpgpath)
        photo.imagefile.name = attachment.otherfile.name[:-4] + '.jpg'
        photo.contributor = request.user
        photo.make_thumbnail()
        photo.save()        
  return HttpResponseRedirect(reverse('demo-detail', args=[attachment.demo.id]))

def convert_pdf(pdfpath, jpgpath):
  result = subprocess.call(['gs','-sDEVICE=jpeg','-dNOPAUSE','-dQUIET','-dBATCH','-r144','-sOutputFile=' + jpgpath,pdfpath])
  if not result:
    return True

# Tag

@login_required
def delete_tag(request, pk):
  tag=get_object_or_404(Tag, pk = pk)
  tag.delete()
  return HttpResponseRedirect(reverse('tags'))                             
                          
@login_required
def manage_tags(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  tags = Tag.objects.values_list('text', flat=True)
  if request.method == 'POST':
    form = TagForm(request.POST)
    if form.is_valid():
      text = form.cleaned_data['text'].lower()
      qs = Tag.objects.filter(text=text)
      if qs:
        demo.tags.add(qs[0])
      else:
        demo.tags.create(text=text)
      form = TagForm()
  else:
    form = TagForm()
  return render(request, 'physics/manage_tags.html', {'form': form, 'demo': demo, 'tags': tags})

@login_required
def demo_delete_tag(request, demo, tag):
  demo=get_object_or_404(Demo, pk = demo)
  tag=get_object_or_404(Tag, pk = tag)
  demo.tags.remove(tag)
  return HttpResponseRedirect(reverse('manage-tags', args=[demo.id]))

# Component

@login_required
def delete_component(request, pk):
  component=get_object_or_404(Component, pk = pk)
  component.delete()
  return HttpResponseRedirect(reverse('components'))                             
                          
@login_required
def manage_components(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  components = Component.objects.values_list('name', flat=True)
  if request.method == 'POST':
    form = TagForm(request.POST)
    if form.is_valid():
      text = form.cleaned_data['text'].lower()
      qs = Component.objects.filter(name=text)
      if qs:
        demo.components.add(qs[0])
      else:
        demo.components.create(name=text)
      form = TagForm()
  else:
    form = TagForm()
  return render(request, 'physics/manage_components.html', {'form': form, 'demo': demo, 'components': components})

@login_required
def demo_delete_component(request, demo, component):
  demo=get_object_or_404(Demo, pk = demo)
  component=get_object_or_404(Component, pk = component)
  demo.components.remove(component)
  return HttpResponseRedirect(reverse('manage-components', args=[demo.id]))

# Note

@login_required
def demo_add_note(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note = Note()
      note.text = form.cleaned_data['text']
      note.contributor = request.user
      note.save()
      demo.notes.add(note)
      return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))
  else:
    form = NoteForm()
  return render(request, 'physics/demo_add_note.html', {'form': form, 'demo': demo})

@login_required
def demo_update_note(request, demo, note):
  demo=get_object_or_404(Demo, pk=demo)
  note=get_object_or_404(Note, pk=note)
  if request.user != note.contributor:
    return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))
  elif request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note.text = form.cleaned_data['text']
      note.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))
  else:
    form = NoteForm(initial={'text': note.text})
  return render(request, 'physics/demo_update_note.html', {'form': form, 'demo': demo, 'note': note})

@login_required
def demo_delete_note(request, demo, note):
  demo=get_object_or_404(Demo, pk=demo)
  note=get_object_or_404(Note, pk=note)
  if note.contributor == request.user:
    note.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demo.id]))

@login_required
def photo_add_note(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  if request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note = Note()
      note.text = form.cleaned_data['text']
      note.contributor = request.user
      note.save()
      photo.notes.add(note)
      return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))
  else:
    form = NoteForm()
  return render(request, 'physics/photo_add_note.html', {'form': form, 'photo': photo})

@login_required
def photo_update_note(request, photo, note):
  photo=get_object_or_404(Photo, pk=photo)
  note=get_object_or_404(Note, pk=note)
  if request.user != note.contributor:
    return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))
  elif request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note.text = form.cleaned_data['text']
      note.save()
      return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))
  else:
    form = NoteForm(initial={'text': note.text})
  return render(request, 'physics/photo_update_note.html', {'form': form, 'photo': photo, 'note': note})

@login_required
def photo_delete_note(request, photo, note):
  photo=get_object_or_404(Photo, pk=photo)
  note=get_object_or_404(Note, pk=note)
  if note.contributor == request.user:
    note.delete()
  return HttpResponseRedirect(reverse('photo-detail', args=[photo.id]))

def test(request):
  text = "blah"
  #tags = Tag.objects.values_list('text', flat=True).distinct()
  obs = Photo.objects.filter(demo__mainphoto=F('id'))
  return render(request, 'physics/test.html', {'obs': obs})


    

  
