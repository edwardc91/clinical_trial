__author__ = 'root'
from django.shortcuts import render
from django import forms
from models import Paciente, Frecuencia,Unidad
from forms import PacienteForm,UnidadForm, FrecuenciaForm

def view_index(request):
    return render(request, 'index.html')

def view_paciente(request):
   frecuencias=[(f.tipo) for f in Frecuencia.objects.using('postgredb1').all()]
   medidas=[(u.medida) for u in Unidad.objects.using('postgredb1').all()]
   if request.POST:

        form = FrecuenciaForm(request.POST,data_list=frecuencias,prefix="Frecuencia")#PacienteForm(request.POST)
        formM= UnidadForm(request.POST,data_list=medidas,prefix="Medida")
        if form.is_valid() and formM.is_valid():
            """iniciales = form.cleaned_data["iniciales"]
            no_inclusion = form.cleaned_data["no_inclusion"]
            fecha_inclusion = form.cleaned_data["fecha_inclusion"]
            edad = form.cleaned_data["edad"]
            sexo = form.cleaned_data["sexo"]
            raza = form.cleaned_data['raza']

            paciente = Paciente.objects.using('postgredb1').create(iniciales=iniciales,
                                                                   no_inclusion=no_inclusion,
                                                                   fecha_inclusion=fecha_inclusion,
                                                                   edad=edad,
                                                                   sexo=sexo,
                                                                   raza=raza)
            paciente.save()"""
            return render(request, 'tests.html', {'paciente_form' : form, 'unidad_form' : formM})
   else:
       form = FrecuenciaForm(data_list=frecuencias,prefix="Frecuencia")#PacienteForm()
       formM=UnidadForm(data_list=medidas,prefix="Medida")

   return render(request, 'tests.html', {'paciente_form' : form, 'unidad_form' : formM})

def home_view(request):
    pacientes = Paciente.objects.using("postgredb1").all().order_by('iniciales')