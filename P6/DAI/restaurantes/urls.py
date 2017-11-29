from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^ai/$', views.ai, name='ai'),
  url(r'^restaurant_search/$', views.restaurant_search, name='restaurant_search'),
  url(r'^get_page/$', views.get_page, name='get_page'),
  url(r'^get_number_of_pages/$', views.get_number_of_pages, name='get_number_of_pages'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.login_view, name='login'),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^profile/$', views.profile, name='profile'),
  url(r'^change_info/$', views.change_info, name='change_info')
]
