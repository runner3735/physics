
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
  #url(r'^tag/(?P<tag>[-\w]+)$', views.demos_by_tag(), name='demos-by-tag'),
  url(r'^myphotos/$', views.MyPhotosListView.as_view(), name='my-photos'),
  url(r'^mainphotos/$', views.DemoPhotoView.as_view(), name='main-photos'),
  
  url(r'^demo/create/$', views.DemoCreate.as_view(), name='demo_create'),
  url(r'^demo/(?P<pk>\d+)/name/$', views.name_update, name='name-update'),
  url(r'^demo/(?P<pk>\d+)/course/$', views.course_update, name='course-update'),
  url(r'^demo/(?P<pk>\d+)/room/$', views.room_update, name='room-update'),
  url(r'^demo/(?P<pk>\d+)/location/$', views.location_update, name='location-update'),
  url(r'^demo/(?P<pk>\d+)/description/$', views.description_update, name='description-update'),
  url(r'^demo/(?P<pk>\d+)/add-photo/$', views.add_photo, name='add-photo'),
  url(r'^demo/(?P<pk>\d+)/add-file/$', views.add_file, name='add-file'),
  
  url(r'^tag/(?P<pk>\d+)/delete/$', views.delete_tag, name='delete-tag'),
  url(r'^demo/(?P<pk>\d+)/manage-tags/$', views.manage_tags, name='manage-tags'),
  #url(r'^demo/(?P<pk>\d+)/add-tag/$', views.demo_add_tag, name='demo-add-tag'),
  url(r'^demo/(?P<demo>\d+)/delete-tag/(?P<tag>\d+)/$', views.demo_delete_tag, name='demo-delete-tag'),
  
  url(r'^component/(?P<pk>\d+)/delete/$', views.delete_component, name='delete-component'),
  url(r'^demo/(?P<pk>\d+)/manage-components/$', views.manage_components, name='manage-components'),
  #url(r'^demo/(?P<pk>\d+)/add-component/$', views.demo_add_component, name='demo-add-component'),
  url(r'^demo/(?P<demo>\d+)/delete-component/(?P<component>\d+)/$', views.demo_delete_component, name='demo-delete-component'),
  
  url(r'^photo/(?P<pk>\d+)$', views.photo_detail, name='photo-detail'),
  url(r'^photo/(?P<pk>\d+)/delete/$', views.delete_photo, name='delete-photo'),
  url(r'^photo/(?P<pk>\d+)/update/$', views.update_photo, name='update-photo'),
  url(r'^photo/(?P<pk>\d+)/main/$', views.main_photo, name='main-photo'),

  url(r'^demo/(?P<pk>\d+)/add-note/$', views.demo_add_note, name='demo-add-note'),
  url(r'^demo/(?P<demo>\d+)/update-note/(?P<note>\d+)/$', views.demo_update_note, name='demo-update-note'),
  url(r'^demo/(?P<demo>\d+)/delete-note/(?P<note>\d+)/$', views.demo_delete_note, name='demo-delete-note'),
  url(r'^photo/(?P<pk>\d+)/add-note/$', views.photo_add_note, name='photo-add-note'),
  url(r'^photo/(?P<photo>\d+)/update-note/(?P<note>\d+)/$', views.photo_update_note, name='photo-update-note'),
  url(r'^photo/(?P<photo>\d+)/delete-note/(?P<note>\d+)/$', views.photo_delete_note, name='photo-delete-note'),
  
  url(r'^attachment/(?P<pk>\d+)/delete/$', views.delete_file, name='delete-file'),
  url(r'^attachment/(?P<pk>\d+)/update/$', views.update_file, name='update-file'),
  url(r'^attachment/(?P<pk>\d+)/convert/$', views.convert_file, name='convert-file'),
  
  url(r'^test/$', views.test, name='test'),
]

