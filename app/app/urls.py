from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
                       url(r'^$', views.get_watershed, name='get_watershed'),
)
