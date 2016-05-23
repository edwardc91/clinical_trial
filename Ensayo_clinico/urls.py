from django.conf.urls import include, url
from django.contrib import admin

from Ensayo_Clinico_App import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ensayo_clinico_old.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^paciente/', views.view_paciente,name="Paciente"),
    url(r'^(?P<no_inc>[0-9]{3})paciente/', views.view_mod_paciente,name="Paciente_modificar"),
    url(r'^(?P<no_inc>[0-9]{3})evaluacion_inicial/', views.view_evaluacion_inicial,name="Evaluacion_inicial"),
    url(r'^(?P<no_inc>[0-9]{3})/(?P<dia>[0-7])/evaluacion_durante/', views.view_evaluacion_durante,name="Evaluacion_durante"),
    url(r'^(?P<no_inc>[0-9]{3})evaluacion_final/', views.view_evaluacion_final,name="Evaluacion_final"),
    url(r'^(?P<no_inc>[0-9]{3})interrupcion_tratamiento/', views.view_interrupcion_tratamiento,name="Interrupcion_tratamiento"),
    url(r'^ensayo_clinico/', views.view_index,name="Index"),
    url(r'^tests/', views.view_tests,name="Tests"),
]
