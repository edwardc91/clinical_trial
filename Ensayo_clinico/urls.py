from django.conf.urls import include, url
from django.contrib import admin

from Ensayo_Clinico_App import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Ensayo_clinico_old.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^paciente/', views.view_paciente,name="Paciente"),
    url(r'^(?P<no_inc>[0-9]{1,2})paciente/', views.view_mod_paciente,name="Paciente_modificar"),
    url(r'^(?P<no_inc>[0-9]{1,2})evaluacion_inicial/', views.view_evaluacion_inicial,name="Evaluacion_inicial"),
    url(r'^(?P<no_inc>[0-9]{1,2})/(?P<dia>[0-7])/evaluacion_durante/', views.view_evaluacion_durante,name="Evaluacion_durante"),
    url(r'^(?P<no_inc>[0-9]{1,2})evaluacion_final/', views.view_evaluacion_final,name="Evaluacion_final"),
    url(r'^(?P<no_inc>[0-9]{1,2})interrupcion_tratamiento/', views.view_interrupcion_tratamiento,name="Interrupcion_tratamiento"),
    url(r'^(?P<no_inc>[0-9]{1,2})eventos_adversos/', views.view_eventos_adversos,name="Eventos_adversos"),
    url(r'^(?P<no_inc>[0-9]{1,2})evento_adverso/', views.view_evento_adverso,name="Evento_adverso"),
    url(r'^(?P<no_inc>[0-9]{1,2})/(?P<evento>[\w\s]+)evento_adverso_mod/', views.view_mod_evento_adverso,name="Evento_adverso_mod"),
    url(r'^(?P<no_inc>[0-9]{1,2})tratamientos_concomitantes/', views.view_tratamientos_concomitantes,name="Tratamientos_concomitantes"),
    url(r'^(?P<no_inc>[0-9]{1,2})tratamiento_concomitante/', views.view_tratamiento_concomitante,name="Tratamiento_concomitante"),
    url(r'^ensayo_clinico/', views.view_index,name="Index"),
    url(r'^tests/', views.view_tests,name="Tests"),
]
