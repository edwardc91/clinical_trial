from django.forms.extras.widgets import SelectDateWidget
__author__ = 'root'

from django.forms import ModelForm
from django import forms
from models import Paciente

class PacienteForm(forms.Form):
    iniciales = forms.CharField(label="Iniciales",max_length=4)
    no_inclusion = forms.IntegerField(label="No. inclusion")
    fecha_inclusion = forms.DateField(label="Fecha inclusion",widget=SelectDateWidget(years=range(2016,2016)))
    edad = forms.IntegerField(label="Edad", max_value=150)
    sexo = forms.ChoiceField(label="Sexo",choices={(1,"Masculino"),(2,"Femenino")},widget=forms.RadioSelect)
    raza = forms.ChoiceField(label="Raza",choices={(1,"Blanca"),(2,"Negra"),(3,"Mestiza"),(4,"Amarilla")},widget=forms.RadioSelect)

class EvaluacionInicialForm(forms.Form):
    fecha = forms.DateField(label="Fecha",widget=SelectDateWidget(years=range(2016,2016)))
    hipertension_arterial=forms.ChoiceField(label="Hipertension Arterial",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    hiperlipidemias = forms.ChoiceField(label="Hiperlipidemias",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    cardiopatia_isquemica=forms.ChoiceField(label="Cardiopatia isquemica",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    ulceras_pies=forms.ChoiceField(label="Historia ulceras pies",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    amputacion_mayor=forms.ChoiceField(label="Amputacion mayor",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    amputacion_menor=forms.ChoiceField(label="Amputacion menor",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    tipo_diabetes=forms.ChoiceField(label="Tipo de Diabetes",choices={(1,"Tipo I"),(2,"Tipo II")},widget=forms.RadioSelect)
    tiempo_evolucion=forms.IntegerField(label="Tiempo Evolucion",max_value=99)
    habito_fumar=forms.ChoiceField(label="Habito fumar",choices={(1,"Fumador"),(2,"Exfumador"),(3,"No fumador")},widget=forms.RadioSelect)
    alcoholismo=forms.ChoiceField(label="Alcoholismo",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    miembro_afectado=forms.ChoiceField(label="Miembro afectado",choices={(1,"Pie derecho"),(2,"Pie izquierdo")},widget=forms.RadioSelect)
    dedos=forms.ChoiceField(label="Dedos",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    dorso_pie=forms.ChoiceField(label="Dorso del pie",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    planta=forms.ChoiceField(label="Planta",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    calcaneo=forms.ChoiceField(label="Calcaneo",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    lateral_interno=forms.ChoiceField(label="Lateral interno",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    laterla_externo=forms.ChoiceField(label="Lateral externo",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    transmetatarsian=forms.ChoiceField(label="Transmetatarsiano",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    clasificacion_idsa=forms.ChoiceField(label="Clasificacion IDSA",choices={(1,"No infeccion"),(2,"Leve"),(3,"Moderado"),(4,"Severo")},widget=forms.RadioSelect)
    cultivo_microbiologico=forms.ChoiceField(label="Cultivo microbiologico",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    tratamiento_concomitante=forms.ChoiceField(label="Tratamiento concomitante",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)

class EvaluacionDuranteForm(forms.Form):
    fecha = forms.DateField(label="Fecha",widget=SelectDateWidget(years=range(2016,2016)))
    previo_diastolica=forms.DecimalField(label="Diastolica previo",max_digits=3,decimal_places=0)
    previo_sistolica=forms.DecimalField(label="Sistolica previo",max_digits=3,decimal_places=0)
    previo_fc=forms.DecimalField(label="FC previo",max_digits=3,decimal_places=0)
    previo_temperatura=forms.DecimalField(label="Temperatura previo",max_digits=3,decimal_places=1)
    despues_diastolica=forms.DecimalField(label="Diastolica despues",max_digits=3,decimal_places=0)
    despues_sistolica=forms.DecimalField(label="Sistolica despues",max_digits=3,decimal_places=0)
    despues_fc=forms.DecimalField(label="FC despues",max_digits=3,decimal_places=0)
    despues_temperatura=forms.DecimalField(label="Temperatura despues",max_digits=3,decimal_places=1)
    glicemia_valor=forms.DecimalField(label="Resultado glicemia",max_digits=3,decimal_places=1)
    glicemia=forms.ChoiceField(label="Glicemia",choices={(1,"No realizado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    fecha_glicemia=forms.DateField(label="Fecha Glicemia",widget=SelectDateWidget(years=range(2016,2016)))
    manifestaciones_clinicas=forms.ChoiceField(label="Manifestaciones clinicas",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    tratamiento_concomitante=forms.ChoiceField(label="Tratamiento concomitante",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    eventos_adversos=forms.ChoiceField(label="Eventos adversos",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    interrumpio_tratamiento=forms.ChoiceField(label="Interrumpio tratamiento",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)

class EvaluacionFinalForm(forms.Form):
    fecha = forms.DateField(label="Fecha",widget=SelectDateWidget(years=range(2016,2016)))
    cultivo_microbiologico=forms.ChoiceField(label="Cultivo microbiologico",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    manifestaciones_clinicas=forms.ChoiceField(label="Manifestaciones clinicas",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    clasificacion_idsa=forms.ChoiceField(label="Clasificacion IDSA",choices={(1,"No infeccion"),(2,"Leve"),(3,"Moderado"),(4,"Severo")},widget=forms.RadioSelect)

class EvaluacionMicrobiologicaForm(forms.Form):
    fecha = forms.DateField(label="Fecha",widget=SelectDateWidget(years=range(2016,2016)))
    resultado=forms.ChoiceField(label="resultado",choices={(1,"Fumador"),(2,"Exfumador"),(3,"No fumador")},widget=forms.RadioSelect)

class ExamenFisicoForm(forms.Form):
    peso=forms.DecimalField(label="Peso",max_digits=4,decimal_places=1)
    cv=forms.ChoiceField(label="CV",choices={(1,"No examinado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    cv_desc=forms.CharField(label="Descripcion CV",max_length=14)
    respiratorio=forms.ChoiceField(label="Respiratorio",choices={(1,"No examinado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    respiratorio_desc=forms.CharField(label="Descripcion respiratorio",max_length=14)
    abdominal=forms.ChoiceField(label="Abdominal",choices={(1,"No examinado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    abdominal_desc=forms.CharField(label="Descripcion CV",max_length=14)
    extremidades=forms.ChoiceField(label="Extremidades",choices={(1,"No examinado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    piel=forms.CharField(label="Piel",max_length=14)
    piel_desc=forms.CharField(label="Piel CV",max_length=14)
    neurologico=forms.ChoiceField(label="Neurologico",choices={(1,"No examinado"),(2,"Normal"),(3,"CS"),(4,"NCS")},widget=forms.RadioSelect)
    neurologico_desc=forms.CharField(label="Desc neurologico",max_length=14)

class ManifestacionesClinicasForm(forms.Form):
    induracion=forms.ChoiceField(label="Induracion",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    edema_local=forms.ChoiceField(label="Edema Local",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    eritema_diametro = forms.DecimalField(label="Diametro del eritema",max_digits=2, decimal_places=1)
    sensibilidad=forms.ChoiceField(label="Sensibilidad",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    dolor_local=forms.ChoiceField(label="Dolor local",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    calor_local=forms.ChoiceField(label="Calor local",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    secrecion_purulenta=forms.ChoiceField(label="Secrecion purulenta",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    secrecion_no_purulenta=forms.ChoiceField(label="Secrecion no purulenta",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)

time_widget = forms.widgets.TimeInput(attrs={'class': 'time-pick'})
valid_time_formats = ['%P', '%H:%M%A', '%H:%M %A', '%H:%M%a', '%H:%M %a']

class TratamientoConcomitanteForm(forms.Form):
    #ver lo de las llaves foraneas
    tratar_eventos_adversos=forms.ChoiceField(label="Para tratar eventos adversos",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    dosis=forms.IntegerField(label="Dosis",max_value=99)
    fecha_inicio=forms.DateField(label="Fecha Inicio",widget=SelectDateWidget(years=range(2016,2016)))
    fecha_fin=forms.DateField(label="Fecha Fin",widget=SelectDateWidget(years=range(2016,2016)))
    duracion_24_horas=forms.TimeField(label="Si duracion menor de 24h",widget=time_widget, help_text='ex: 10:30AM', input_formats=valid_time_formats)

class NecrociaForms(forms.Form):
    hallazgo1=forms.CharField(label="Hallazgo 1",max_length=26)
    hallazgo2=forms.CharField(label="Hallazgo 2",max_length=26)
    hallazgo3=forms.CharField(label="Hallazgo 3",max_length=26)

class Interrupciontratamiento(forms.Form):
    fecha=forms.DateField(label="Fecha Inicio",widget=SelectDateWidget(years=range(2016,2016)))
    dosis_recibidas=forms.IntegerField(label="Dosis recibidas",max_value=9)
    abandono_voluntario=forms.ChoiceField(label="Abandono voluntario",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    criterios_exclusion=forms.ChoiceField(label="Criterios de exclusion",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    eventos_adversos=forms.ChoiceField(label="Eventos adversos",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    aparicion_agravamiento=forms.ChoiceField(label="Agravamiento",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)
    fallecimento=forms.ChoiceField(label="Fallecimiento",choices={(1,"Si"),(2,"No")},widget=forms.RadioSelect)