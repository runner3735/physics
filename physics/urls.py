
from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^demos/$', views.DemoListView.as_view(), name='demos'),
  url(r'^demo/(?P<pk>\d+)$', views.DemoDetailView.as_view(), name='demo-detail'),
  url(r'^courses/$', views.CourseListView.as_view(), name='courses'),
  url(r'^course/(?P<pk>\d+)$', views.CourseDetailView.as_view(), name='course-detail'),
  url(r'^rooms/$', views.RoomListView.as_view(), name='rooms'),
  url(r'^room/(?P<pk>\d+)$', views.RoomDetailView.as_view(), name='room-detail'),
  url(r'^myphotos/$', views.MyPhotosListView.as_view(), name='my-photos'),
  url(r'^demo/(?P<pk>\d+)/name/$', views.name_update, name='name-update'),
  url(r'^demo/(?P<pk>\d+)/course/$', views.course_update, name='course-update'),
  url(r'^demo/(?P<pk>\d+)/room/$', views.room_update, name='room-update'),
  url(r'^demo/(?P<pk>\d+)/location/$', views.location_update, name='location-update'),
  url(r'^demo/(?P<pk>\d+)/description/$', views.description_update, name='description-update'),
  url(r'^demo/(?P<pk>\d+)/tags/$', views.manage_tags, name='manage-tags'),
  url(r'^demo/create/$', views.DemoCreate.as_view(), name='demo_create'),
  url(r'^demo/(?P<pk>\d+)/update/$', views.DemoUpdate.as_view(), name='demo_update'),
  url(r'^demo/(?P<pk>\d+)/delete/$', views.DemoDelete.as_view(), name='demo_delete'),
  url(r'^demo/(?P<pk>\d+)/addphoto/$', views.add_photo, name='add-photo'),
  url(r'^demo/(?P<pk>\d+)/addnote/$', views.add_note, name='add-note'),
  url(r'^demo/(?P<pk>\d+)/addtag/$', views.add_tag, name='add-tag'),
  url(r'^demo/(?P<pk>\d+)/addfile/$', views.add_file, name='add-file'),
  url(r'^note/(?P<pk>\d+)/delete/$', views.delete_note, name='delete-note'),
  url(r'^tag/(?P<pk>\d+)/delete/$', views.delete_tag, name='delete-tag'),
  url(r'^note/(?P<pk>\d+)/update/$', views.update_note, name='update-note'),
  url(r'^photo/(?P<pk>\d+)/delete/$', views.delete_photo, name='delete-photo'),
  url(r'^photo/(?P<pk>\d+)/update/$', views.update_photo, name='update-photo'),
  url(r'^photo/(?P<pk>\d+)/main/$', views.main_photo, name='main-photo'),
  url(r'^attachment/(?P<pk>\d+)/delete/$', views.delete_file, name='delete-file'),
  url(r'^attachment/(?P<pk>\d+)/update/$', views.update_file, name='update-file'),
  url(r'^test/$', views.test, name='test'),
]

