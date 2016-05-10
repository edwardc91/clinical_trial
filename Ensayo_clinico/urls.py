from django.conf.urls import include, url
from django.contrib import admin

from Ensayo_Clinico_App import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ensayo_clinico_old.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^paciente/', views.view_paciente,name="Paciente"),
    url(r'^ensayo_clinico/', views.view_index,name="Index"),
]
