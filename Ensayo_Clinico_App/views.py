__author__ = 'root'
from django.shortcuts import render
from django import forms
from models import Paciente
from forms import PacienteForm

def view_paciente(request):
   if request.POST:
        form = PacienteForm(request.POST)
        if form.is_valid():
            iniciales = form.cleaned_data["iniciales"]
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
            paciente.save()
            return render(request, 'paciente.html', {'paciente_form' : form})
   else:
       form = PacienteForm()

   return render(request, 'paciente.html', {'paciente_form' : form})

def home_view(request):
    pacientes = Paciente.objects.using("postgredb1").all().order_by('iniciales')