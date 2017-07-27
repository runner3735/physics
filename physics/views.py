
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Course, Demo, Photo, Room, Note, Attachment, Keyword
from .forms import NameForm, DescriptionForm, CourseForm, RoomForm, LocationForm, DemoForm, NoteForm, TagForm
from .forms import NewPhotoForm, UpdatePhotoForm, NewFileForm, UpdateFileForm

def index(request):
  num_demos = Demo.objects.all().count()
  num_photos = Photo.objects.all().count()
  return render(request, 'index.html', context={'num_demos':num_demos,'num_photos':num_photos})
  
class DemoListView(generic.ListView):
  model = Demo
  paginate_by = 20

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
    #form = CourseForm()
  return render(request, 'physics/course_update.html', {'form': form, 'demo': demo})

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

def manage_tags(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  return render(request, 'physics/manage_tags.html', {'demo': demo})

def test(request):
  text = "blah"
  q = Keyword.objects.values_list('text', flat=True).distinct()
  return render(request, 'physics/test.html', {'test': q})

#@permission_required('physics.can_update_demos')
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
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = NewPhotoForm()
  return render(request, 'physics/new_photo.html', {'form': form, 'demo': demo})

def update_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  if request.method == 'POST':
    form = UpdatePhotoForm(request.POST, request.FILES)
    if form.is_valid():
      photo.caption = form.cleaned_data['caption']
      if form.cleaned_data['imagefile']:
        photo.delete_images()
        photo.imagefile = form.cleaned_data['imagefile']
        photo.make_thumbnail()
      photo.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[photo.demo.id]))
  else:
    form = UpdatePhotoForm(initial={'caption': photo.caption})
  return render(request, 'physics/update_photo.html', {'form': form, 'photo': photo})

def delete_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  demopk = photo.demo.id
  if photo.contributor == request.user:
    photo.delete_images()
    photo.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demopk]))

def main_photo(request, pk):
  photo=get_object_or_404(Photo, pk = pk)
  photo.demo.mainphoto = pk
  photo.demo.save()
  return HttpResponseRedirect(reverse('demo-detail', args=[photo.demo.id]))

def add_file(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NewFileForm(request.POST, request.FILES)
    if form.is_valid():
      attachment = Attachment()
      attachment.demo = demo
      attachment.description = form.cleaned_data['description']
      attachment.otherfile = form.cleaned_data['otherfile']
      attachment.contributor = request.user
      attachment.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = NewFileForm()
  return render(request, 'physics/new_file.html', {'form': form, 'demo': demo})

def update_file(request, pk):
  attachment=get_object_or_404(Attachment, pk = pk)
  if request.method == 'POST':
    form = UpdateFileForm(request.POST, request.FILES)
    if form.is_valid():
      attachment.description = form.cleaned_data['description']
      if form.cleaned_data['otherfile']:
        attachment.otherfile = form.cleaned_data['otherfile']
      attachment.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[attachment.demo.id]))
  else:
    form = UpdateFileForm(initial={'description': attachment.description})
  return render(request, 'physics/update_file.html', {'form': form, 'attachment': attachment})

def delete_file(request, pk):
  attachment=get_object_or_404(Attachment, pk = pk)
  demopk = attachment.demo.id
  if attachment.contributor == request.user:
    attachment.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demopk]))

def add_tag(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = TagForm(request.POST)
    if form.is_valid():
      tag = Keyword()
      tag.demo = demo
      tag.text = form.cleaned_data['text']
      tag.save()
      return HttpResponseRedirect(reverse('manage-tags', args=[pk]))
  else:
    form = TagForm()
  return render(request, 'physics/new_tag.html', {'form': form, 'demo': demo})

def add_note(request, pk):
  demo=get_object_or_404(Demo, pk = pk)
  if request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note = Note()
      note.demo = demo
      note.text = form.cleaned_data['text']
      note.contributor = request.user
      note.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[pk]))
  else:
    form = NoteForm()
  return render(request, 'physics/new_note.html', {'form': form, 'demo': demo})

def update_note(request, pk):
  note=get_object_or_404(Note, pk = pk)
  if request.method == 'POST':
    form = NoteForm(request.POST)
    if form.is_valid():
      note.text = form.cleaned_data['text']
      note.save()
      return HttpResponseRedirect(reverse('demo-detail', args=[note.demo.id]))
  else:
    form = NoteForm(initial={'text': note.text,})
  return render(request, 'physics/update_note.html', {'form': form, 'note': note})

def delete_note(request, pk):
  note=get_object_or_404(Note, pk = pk)
  demopk = note.demo.id
  if note.contributor == request.user:
    note.delete()
  return HttpResponseRedirect(reverse('demo-detail', args=[demopk]))

def delete_tag(request, pk):
  tag=get_object_or_404(Keyword, pk = pk)
  demopk = tag.demo.id
  tag.delete()
  return HttpResponseRedirect(reverse('manage-tags', args=[demopk]))

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class DemoCreate(CreateView):
  model = Demo
  form_class = DemoForm
  #initial={'description':'Insert a full description of the demo here.',}

class DemoUpdate(UpdateView):
  model = Demo
  fields = '__all__'
  #fields = ['first_name','last_name','date_of_birth','date_of_death']

class DemoDelete(DeleteView):
  model = Demo
  success_url = reverse_lazy('demos')
    

  
