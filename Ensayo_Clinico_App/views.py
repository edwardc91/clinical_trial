__author__ = 'root'
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
import json, simplejson

from Users_App.models import UserInfo

import models
import forms
import csv


@csrf_exempt
def view_evento_delete_ajax(request, no_inc, nombre):
    evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                       nombre=nombre)

    if evento_adverso.exists():
        evento_adverso = evento_adverso[0]
        evento_adverso.delete()

        return HttpResponse(json.dump(nombre), content_type="application/json")


def view_home(request):
    if request.POST:
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']

            user = authenticate(username=usuario, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('Index'))
            else:
                return render(request, "home.html", {'form': form})

    form = forms.LoginForm()
    context = {'form': form}
    return render(request, "home.html", context)


def view_login(request):
    if request.POST:
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            password = form.cleaned_data['password']

            user = authenticate(username=usuario, password=password)

            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('Index'))
            else:
                return render(request, "login.html", {'form': form})
    else:
        form = forms.LoginForm()

    context = {'form': form}
    return render(request, "login.html", context)


def view_logout(request):
    logout(request)
    # form = forms.LoginForm()
    return HttpResponseRedirect(reverse('Login'))


@login_required
def view_index(request):
    user = request.user.username
    if request.POST:
        if 'inc_pac' in request.POST:
            no_inc = request.POST['inc_pac']
            try:
                usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
                paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
                paciente.delete()
                context = {'status': 'True', 'no_inc': no_inc}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")

    return render(request, 'index.html', list_pacientes(user))


def view_tests(request):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    frecuencias = [(f.tipo) for f in models.Frecuencia.objects.using(usuario_database).all()]
    medidas = [(u.medida) for u in models.Unidad.objects.using(usuario_database).all()]
    if request.POST:

        form = forms.FrecuenciaForm(request.POST, data_list=frecuencias,
                                    prefix="Frecuencia")  # PacienteForm(request.POST)
        formM = forms.UnidadForm(request.POST, data_list=medidas, prefix="Medida")
        if form.is_valid() and formM.is_valid():
            return render(request, 'tests.html', {'paciente_form': form, 'unidad_form': formM})
    else:
        form = forms.FrecuenciaForm(data_list=frecuencias, prefix="Frecuencia")  # PacienteForm()
        formM = forms.UnidadForm(data_list=medidas, prefix="Medida")

    return render(request, 'tests.html', {'paciente_form': form, 'unidad_form': formM})


def list_pacientes(user):
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    pacientes = models.Paciente.objects.using(usuario_database).all().order_by('no_inclusion')
    context = {'pacientes': pacientes}
    return context


@login_required
def view_paciente(request):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    result = "Datos del paciente"

    if request.POST:
        form = forms.PacienteForm(request.POST)
        if form.is_valid():
            iniciales = form.cleaned_data["iniciales"]
            no_inclusion = form.cleaned_data["no_inclusion"]
            fecha_inclusion = form.cleaned_data["fecha_inclusion"]
            edad = form.cleaned_data["edad"]
            sexo = form.cleaned_data["sexo"]
            raza = form.cleaned_data['raza']

            paciente = models.Paciente.objects.using(usuario_database).create(iniciales=iniciales,
                                                                              no_inclusion=no_inclusion,
                                                                              fecha_inclusion=fecha_inclusion,
                                                                              edad=edad,
                                                                              sexo=sexo,
                                                                              raza=raza)
            paciente.save()
            result = "Introducidos los datos del paciente " + paciente.iniciales + " exitosamente"
            return HttpResponseRedirect(reverse('Paciente_modificar', args=(no_inclusion,)))
    else:
        form = forms.PacienteForm()
    return render(request, 'paciente.html', {'paciente_form': form, 'result': result})


@login_required
def view_mod_paciente(request, no_inc):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = 0

    if request.POST:
        form = forms.PacienteForm(request.POST)
        if form.is_valid():
            iniciales = form.cleaned_data["iniciales"]
            no_inclusion = form.cleaned_data["no_inclusion"]
            fecha_inclusion = form.cleaned_data["fecha_inclusion"]
            edad = form.cleaned_data["edad"]
            sexo = form.cleaned_data["sexo"]
            raza = form.cleaned_data['raza']

            paciente.iniciales = iniciales
            paciente.no_inclusion = no_inclusion
            paciente.fecha_inclusion = fecha_inclusion
            paciente.edad = edad
            paciente.sexo = sexo
            paciente.raza = raza

            paciente.save()
            """if no_inc != no_inclusion:
                paciente_old=Paciente.objects.using(usuario_database).filter(no_inclusion=no_inc)
                paciente_old.delete()"""

            result = 1
            return render(request, 'paciente_mod.html',
                          {'paciente_form': form, 'inc': no_inclusion, 'result': result, 'paciente': paciente})
        else:
            result = 2

    else:
        paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
        p_data = {'no_inclusion': paciente.no_inclusion,
                  'fecha_inclusion': paciente.fecha_inclusion,
                  'edad': paciente.edad,
                  'sexo': paciente.sexo,
                  'raza': paciente.raza,
                  'iniciales': paciente.iniciales}
        form = forms.PacienteForm(initial=p_data)
    return render(request, 'paciente_mod.html',
                  {'paciente_form': form, 'inc': paciente.no_inclusion, 'result': result, 'paciente': paciente})


@login_required
def view_evaluacion_inicial(request, no_inc):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    exist = True
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = 0

    try:
        init_eval = models.EvaluacionInicial.objects.using(usuario_database).get(no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion inicial del paciente " + paciente.iniciales
        # print "Error"

    examen_fisico = models.ExamenFisico.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=0)
    eval_micro = models.EvaluacionMicrobiologica.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                        dia=0
                                                                                        )
    lab_clinico = models.ExamenLabClinico.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=0)

    mani_clinicas = models.ManifestacionesClinicas.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                          dia=0)

    otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using(usuario_database).filter(
        no_inclusion=no_inc,
        dia=0
    )

    germenes = models.RelacionPacienteGermen.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=0)

    if request.POST:

        form = forms.EvaluacionInicialForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        form4 = forms.EvaluacionMicrobiologicaForm(request.POST)
        form5 = forms.ExamenLabClinicoForm(request.POST)
        form6 = forms.ManifestacionesClinicasOtrasForm(request.POST)
        form7 = forms.GermenForm(request.POST)

        form6.no_inc = no_inc
        form6.dia = 0
        form6.user = user

        form7.no_inc = no_inc
        form7.dia = 0
        form7.user = user

        if "nombre_mani" in request.POST:
            nombre = request.POST['nombre_mani']
            try:
                mani = models.RelacionPacManiClinOtras.objects.using(usuario_database).get(no_inclusion=no_inc, dia=0,
                                                                                           nombre=nombre)
                mani.delete()
                context = {'status': 'True', 'nombre': nombre}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")

        else:
            if "nombre_ger" in request.POST:
                nombre = request.POST['nombre_ger']
                try:
                    germen = models.RelacionPacienteGermen.objects.using(usuario_database).get(no_inclusion=no_inc,
                                                                                               dia=0,
                                                                                               nombre=nombre)
                    germen.delete()
                    context = {'status': 'True', 'nombre': nombre}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
                except:
                    context = {'status': 'False'}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
            else:
                if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid() and form7.is_valid():
                    update_datos_generales_evaluacion_inicial(form=form, exist=exist, init_eval=init_eval,
                                                              paciente=paciente, usuario_database=usuario_database)
                    update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=0,
                                         usuario_database=usuario_database)

                    update_manifestaciones_clinicas(form=form3, mani_clinicas=mani_clinicas, paciente=paciente, dia=0,
                                                    usuario_database=usuario_database)
                    update_evaluacion_microbiologica(form=form4, eval_micro=eval_micro, paciente=paciente, dia=0,
                                                     usuario_database=usuario_database)
                    update_examen_lab_clinico(form=form5, lab_clinico=lab_clinico, paciente=paciente, dia=0,
                                              usuario_database=usuario_database)

                    update_otras_manifestaciones_clinicas(form=form6, paciente=paciente, dia=0,
                                                          usuario_database=usuario_database)
                    update_germenes(form=form7, paciente=paciente, dia=0, usuario_database=usuario_database)
                    # result = "Modificados los datos de la evaluacion inicial de paciente " + paciente.iniciales + " satisfactoriamente"

                    result = 1
                    return render(request, "eval_inicial.html",
                                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5,
                                   'form6': form6,
                                   'form7': form7, 'result': result, 'inc': no_inc, 'paciente': paciente,
                                   'otras_mani': otras_manifestaciones, 'germenes': germenes})
                else:
                    result = 2
    else:
        if exist:
            i_data = {'fecha': init_eval.fecha,
                      'hipertension_arterial': init_eval.hipertension_arterial,
                      'hiperlipidemias': init_eval.hiperlipidemias,
                      'cardiopatia_isquemica': init_eval.cardiopatia_isquemica,
                      'historia_ulcera_pies': init_eval.historia_ulcera_pies,
                      'historia_amputacion': init_eval.historia_amputacion,
                      'amputacion_mayor': init_eval.amputacion_mayor,
                      'amputacion_menor': init_eval.amputacion_menor,
                      'tipo_diabetes': init_eval.tipo_diabetes,
                      'tiempo_evolucion': init_eval.tiempo_evolucion,
                      'habito_fumar': init_eval.habito_fumar,
                      'alcoholismo': init_eval.alcoholismo,
                      'miembro_afectado': init_eval.miembro_afectado,
                      'dedos': init_eval.dedos,
                      'dorso_pie': init_eval.dorso_pie,
                      'planta': init_eval.planta,
                      'calcaneo': init_eval.calcaneo,
                      'lateral_interno': init_eval.lateral_interno,
                      'lateral_externo': init_eval.lateral_externo,
                      'transmetatarsiano': init_eval.transmetatarsiano,
                      'clasificacion_idsa': init_eval.clasificacion_idsa,
                      'cultivo_microbiologico': init_eval.cultivo_microbiologico,
                      'tratamiento_concomitante': init_eval.tratamiento_concomitante
                      }
            form = forms.EvaluacionInicialForm(initial=i_data)
        else:
            form = forms.EvaluacionInicialForm()

        if examen_fisico.exists():
            examen_fisico = examen_fisico[0]

            i_data = {'peso': examen_fisico.peso,
                      'cv': examen_fisico.cv,
                      'cv_desc': examen_fisico.cv_desc,
                      'respiratorio': examen_fisico.respiratorio,
                      'respiratorio_desc': examen_fisico.respiratorio_desc,
                      'abdominal': examen_fisico.abdominal,
                      'abdominal_desc': examen_fisico.abdominal_desc,
                      'extremidades': examen_fisico.extremidades,
                      'extremidades_desc': examen_fisico.extremidades_desc,
                      'piel': examen_fisico.piel,
                      'piel_desc': examen_fisico.piel_desc,
                      'neurologico': examen_fisico.neurologico,
                      'neurologico_desc': examen_fisico.neurologico_desc
                      }

            form2 = forms.ExamenFisicoForm(initial=i_data)
        else:
            form2 = forms.ExamenFisicoForm()

        if mani_clinicas.exists():
            mani_clinicas = mani_clinicas[0]

            i_data = {'induracion': mani_clinicas.induracion,
                      'edema_local': mani_clinicas.edema_local,
                      'eritema_diametro': mani_clinicas.eritema_diametro,
                      'sensibilidad': mani_clinicas.sensibilidad,
                      'dolor_local': mani_clinicas.dolor_local,
                      'calor_local': mani_clinicas.calor_local,
                      'secrecion_purulenta': mani_clinicas.secrecion_purulenta,
                      'secrecion_no_purulenta': mani_clinicas.secrecion_no_purulenta}

            form3 = forms.ManifestacionesClinicasForm(initial=i_data)
        else:
            form3 = forms.ManifestacionesClinicasForm()

        if eval_micro.exists():
            eval_micro = eval_micro[0]

            i_data = {'fecha': eval_micro.fecha,
                      'resultado': eval_micro.resultado}

            form4 = forms.EvaluacionMicrobiologicaForm(initial=i_data)
        else:
            form4 = forms.EvaluacionMicrobiologicaForm()

        if lab_clinico.exists():
            lab_clinico = lab_clinico[0]

            i_data = {'fecha_hematologicos': lab_clinico.fecha_hematologicos,
                      'hemoglobina': lab_clinico.hemoglobina,
                      'hemoglobina_valor': lab_clinico.hemoglobina_valor,
                      'ctl': lab_clinico.ctl,
                      'ctl_valor': lab_clinico.ctl_valor,
                      'neutrofilos': lab_clinico.neutrofilos,
                      'neutrofilos_valor': lab_clinico.neutrofilos_valor,
                      'linfocitos': lab_clinico.linfocitos,
                      'linfocitos_valor': lab_clinico.linfocitos_valor,
                      'monocitos': lab_clinico.monocitos,
                      'monocitos_valor': lab_clinico.monocitos_valor,
                      'eosinofilos': lab_clinico.eosinofilos,
                      'eosinofilos_valor': lab_clinico.eosinofilos_valor,
                      'basofilos': lab_clinico.basofilos,
                      'basofilos_valor': lab_clinico.basofilos_valor,
                      'c_plaquetas': lab_clinico.c_plaquetas,
                      'c_plaquetas_valor': lab_clinico.c_plaquetas_valor,
                      'eritro': lab_clinico.eritro,
                      'eritro_valor': lab_clinico.eritro_valor,
                      'fecha_quimica_sanguinea': lab_clinico.fecha_quimica_sanguinea,
                      'creatinina': lab_clinico.creatinina,
                      'creatinina_valor': lab_clinico.creatinina_valor,
                      'tgo': lab_clinico.tgo,
                      'tgo_valor': lab_clinico.tgo_valor,
                      'tgp': lab_clinico.tgp,
                      'tgp_valor': lab_clinico.tgp_valor,
                      'glicemia': lab_clinico.glicemia,
                      'glicemia_valor': lab_clinico.glicemia_valor
                      }

            form5 = forms.ExamenLabClinicoForm(initial=i_data)
        else:
            form5 = forms.ExamenLabClinicoForm()

        form6 = forms.ManifestacionesClinicasOtrasForm()
        form7 = forms.GermenForm()

    return render(request, "eval_inicial.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6,
                   'form7': form7, 'result': result,
                   'inc': no_inc, 'paciente': paciente, 'otras_mani': otras_manifestaciones, 'germenes': germenes})


def update_germenes(form, paciente, dia, usuario_database):
    nombre = form.cleaned_data['nombre']

    if nombre:
        germen = models.Germen.objects.using(usuario_database).filter(nombre=nombre)
        if germen.exists():
            relacion = models.RelacionPacienteGermen.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                            dia=dia,
                                                                                            nombre=germen[0])
            relacion.save()
        else:
            germen = models.Germen.objects.using(usuario_database).create(nombre=nombre)
            germen.save()
            relacion = models.RelacionPacienteGermen.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                            dia=dia,
                                                                                            nombre=germen)
            relacion.save()


def update_otras_manifestaciones_clinicas(form, paciente, dia, usuario_database):
    otra1 = form.cleaned_data['otra1']
    otra2 = form.cleaned_data['otra2']
    otra3 = form.cleaned_data['otra3']

    if otra1:
        otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).filter(nombre=otra1)
        if otra_mani.exists():
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani[0])
            relacion.save()
        else:
            otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).create(nombre=otra1)
            otra_mani.save()
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani)
            relacion.save()

    if otra2:
        otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).filter(nombre=otra2)
        if otra_mani.exists():
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani[0])
            relacion.save()
        else:
            otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).create(nombre=otra2)
            otra_mani.save()
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani)
            relacion.save()

    if otra3:
        otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).filter(nombre=otra3)
        if otra_mani.exists():
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani[0])
            relacion.save()
        else:
            otra_mani = models.ManifestacionesClinicasOtras.objects.using(usuario_database).create(nombre=otra3)
            otra_mani.save()
            relacion = models.RelacionPacManiClinOtras.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              nombre=otra_mani)
            relacion.save()


def update_datos_generales_evaluacion_inicial(form, exist, init_eval, paciente, usuario_database):
    fecha = form.cleaned_data['fecha']
    hipertension_arterial = form.cleaned_data['hipertension_arterial']
    hiperlipidemias = form.cleaned_data['hiperlipidemias']
    cardiopatia_isquemica = form.cleaned_data['cardiopatia_isquemica']
    historia_ulcera_pies = form.cleaned_data['historia_ulcera_pies']
    historia_amputacion = form.cleaned_data['historia_amputacion']
    amputacion_mayor = form.cleaned_data['amputacion_mayor']
    amputacion_menor = form.cleaned_data['amputacion_menor']
    tipo_diabetes = form.cleaned_data['tipo_diabetes']
    tiempo_evolucion = form.cleaned_data['tiempo_evolucion']
    habito_fumar = form.cleaned_data['habito_fumar']
    alcoholismo = form.cleaned_data['alcoholismo']
    miembro_afectado = form.cleaned_data['miembro_afectado']
    dedos = form.cleaned_data['dedos']
    dorso_pie = form.cleaned_data['dorso_pie']
    planta = form.cleaned_data['planta']
    calcaneo = form.cleaned_data['calcaneo']
    lateral_interno = form.cleaned_data['lateral_interno']
    lateral_externo = form.cleaned_data['lateral_externo']
    transmetatarsiano = form.cleaned_data['transmetatarsiano']
    clasificacion_idsa = form.cleaned_data['clasificacion_idsa']
    cultivo_microbiologico = form.cleaned_data['cultivo_microbiologico']
    tratamiento_concomitante = form.cleaned_data['tratamiento_concomitante']

    if exist:
        print "updated generales evaluacion inicial"
        init_eval.no_inclusion = paciente
        init_eval.fecha = fecha
        init_eval.hipertension_arterial = hipertension_arterial
        init_eval.hiperlipidemias = hiperlipidemias
        init_eval.cardiopatia_isquemica = cardiopatia_isquemica
        init_eval.historia_ulcera_pies = historia_ulcera_pies
        init_eval.historia_amputacion = historia_amputacion
        init_eval.amputacion_mayor = amputacion_mayor
        init_eval.amputacion_menor = amputacion_menor
        init_eval.tipo_diabetes = tipo_diabetes
        init_eval.tiempo_evolucion = tiempo_evolucion
        init_eval.habito_fumar = habito_fumar
        init_eval.alcoholismo = alcoholismo
        init_eval.miembro_afectado = miembro_afectado
        init_eval.dedos = dedos
        init_eval.dorso_pie = dorso_pie
        init_eval.planta = planta
        init_eval.calcaneo = calcaneo
        init_eval.lateral_interno = lateral_interno
        init_eval.lateral_externo = lateral_externo
        init_eval.transmetatarsiano = transmetatarsiano
        init_eval.clasificacion_idsa = clasificacion_idsa
        init_eval.cultivo_microbiologico = cultivo_microbiologico
        init_eval.tratamiento_concomitante = tratamiento_concomitante

        init_eval.save()
    else:
        print "created"
        init_eval = models.EvaluacionInicial.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                    fecha=fecha,
                                                                                    hipertension_arterial=hipertension_arterial,
                                                                                    hiperlipidemias=hiperlipidemias,
                                                                                    cardiopatia_isquemica=cardiopatia_isquemica,
                                                                                    historia_ulcera_pies=historia_ulcera_pies,
                                                                                    historia_amputacion=historia_amputacion,
                                                                                    amputacion_mayor=amputacion_mayor,
                                                                                    amputacion_menor=amputacion_menor,
                                                                                    tipo_diabetes=tipo_diabetes,
                                                                                    tiempo_evolucion=tiempo_evolucion,
                                                                                    habito_fumar=habito_fumar,
                                                                                    alcoholismo=alcoholismo,
                                                                                    miembro_afectado=miembro_afectado,
                                                                                    dedos=dedos,
                                                                                    dorso_pie=dorso_pie,
                                                                                    planta=planta,
                                                                                    calcaneo=calcaneo,
                                                                                    lateral_interno=lateral_interno,
                                                                                    lateral_externo=lateral_externo,
                                                                                    transmetatarsiano=transmetatarsiano,
                                                                                    clasificacion_idsa=clasificacion_idsa,
                                                                                    cultivo_microbiologico=cultivo_microbiologico,
                                                                                    tratamiento_concomitante=tratamiento_concomitante
                                                                                    )
        init_eval.save()


def update_examen_fisico(form, examen_fisico, paciente, dia, usuario_database):
    peso = form.cleaned_data['peso']
    cv = form.cleaned_data['cv']
    cv_desc = form.cleaned_data['cv_desc']
    respiratorio = form.cleaned_data['respiratorio']
    respiratorio_desc = form.cleaned_data['respiratorio_desc']
    abdominal = form.cleaned_data['abdominal']
    abdominal_desc = form.cleaned_data['abdominal_desc']
    extremidades = form.cleaned_data['extremidades']
    extremidades_desc = form.cleaned_data['extremidades_desc']
    piel = form.cleaned_data['piel']
    piel_desc = form.cleaned_data['piel_desc']
    neurologico = form.cleaned_data['neurologico']
    neurologico_desc = form.cleaned_data['neurologico_desc']

    if examen_fisico.exists():
        print "updated"
        examen_fisico = examen_fisico[0]

        examen_fisico.no_inclusion = paciente
        examen_fisico.peso = peso
        examen_fisico.cv = cv
        examen_fisico.cv_desc = cv_desc
        examen_fisico.respiratorio = respiratorio
        examen_fisico.respiratorio_desc = respiratorio_desc
        examen_fisico.abdominal = abdominal
        examen_fisico.abdominal_desc = abdominal_desc
        examen_fisico.extremidades = extremidades
        examen_fisico.extremidades_desc = extremidades_desc
        examen_fisico.piel = piel
        examen_fisico.piel_desc = piel_desc
        examen_fisico.neurologico = neurologico
        examen_fisico.neurologico_desc = neurologico_desc

        examen_fisico.save()
    else:
        print "created"
        examen_fisico = models.ExamenFisico.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                   dia=dia,
                                                                                   peso=peso,
                                                                                   cv=cv,
                                                                                   cv_desc=cv_desc,
                                                                                   respiratorio=respiratorio,
                                                                                   respiratorio_desc=respiratorio_desc,
                                                                                   abdominal=abdominal,
                                                                                   abdominal_desc=abdominal_desc,
                                                                                   extremidades=extremidades,
                                                                                   extremidades_desc=extremidades_desc,
                                                                                   piel=piel,
                                                                                   piel_desc=piel_desc,
                                                                                   neurologico=neurologico,
                                                                                   neurologico_desc=neurologico_desc
                                                                                   )
        examen_fisico.save()


def update_manifestaciones_clinicas(form, mani_clinicas, paciente, dia, usuario_database):
    induracion = form.cleaned_data['induracion']
    edema_local = form.cleaned_data['edema_local']
    eritema_diametro = form.cleaned_data['eritema_diametro']
    sensibilidad = form.cleaned_data['sensibilidad']
    dolor_local = form.cleaned_data['dolor_local']
    calor_local = form.cleaned_data['calor_local']
    secrecion_purulenta = form.cleaned_data['secrecion_purulenta']
    secrecion_no_purulenta = form.cleaned_data['secrecion_no_purulenta']

    if mani_clinicas.exists():
        print "updated manifestaciones clinicas--dia-" + str(dia) + "--paciente--" + paciente.iniciales
        mani_clinicas = mani_clinicas[0]

        mani_clinicas.no_inclusion = paciente
        mani_clinicas.induracion = induracion
        mani_clinicas.edema_local = edema_local
        mani_clinicas.eritema_diametro = eritema_diametro
        mani_clinicas.sensibilidad = sensibilidad
        mani_clinicas.dolor_local = dolor_local
        mani_clinicas.calor_local = calor_local
        mani_clinicas.secrecion_purulenta = secrecion_purulenta
        mani_clinicas.secrecion_no_purulenta = secrecion_no_purulenta

        mani_clinicas.save()
    else:
        print "created manifestaciones_clinicas--dia-" + str(dia) + "--paciente--" + paciente.iniciales
        mani_clinicas = models.ManifestacionesClinicas.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                              dia=dia,
                                                                                              induracion=induracion,
                                                                                              edema_local=edema_local,
                                                                                              eritema_diametro=eritema_diametro,
                                                                                              sensibilidad=sensibilidad,
                                                                                              dolor_local=dolor_local,
                                                                                              calor_local=calor_local,
                                                                                              secrecion_purulenta=secrecion_purulenta,
                                                                                              secrecion_no_purulenta=secrecion_no_purulenta
                                                                                              )
        mani_clinicas.save()


def update_evaluacion_microbiologica(form, eval_micro, paciente, dia, usuario_database):
    fecha = form.cleaned_data['fecha']
    resultado = form.cleaned_data['resultado']

    if eval_micro.exists():
        # print "updated"
        eval_micro = eval_micro[0]

        eval_micro.no_inclusion = paciente
        eval_micro.fecha = fecha
        eval_micro.resultado = resultado

        eval_micro.save()
    else:
        # print "created"
        eval_micro = models.EvaluacionMicrobiologica.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                            dia=dia,
                                                                                            fecha=fecha,
                                                                                            resultado=resultado
                                                                                            )
        eval_micro.save()


def update_examen_lab_clinico(form, lab_clinico, paciente, dia, usuario_database):
    fecha_hematologicos = form.cleaned_data['fecha_hematologicos']
    hemoglobina = form.cleaned_data['hemoglobina']
    hemoglobina_valor = form.cleaned_data['hemoglobina_valor']
    ctl = form.cleaned_data['ctl']
    ctl_valor = form.cleaned_data['ctl_valor']
    neutrofilos = form.cleaned_data['neutrofilos']
    neutrofilos_valor = form.cleaned_data['neutrofilos_valor']
    linfocitos = form.cleaned_data['linfocitos']
    linfocitos_valor = form.cleaned_data['linfocitos_valor']
    monocitos = form.cleaned_data['monocitos']
    monocitos_valor = form.cleaned_data['monocitos_valor']
    eosinofilos = form.cleaned_data['eosinofilos']
    eosinofilos_valor = form.cleaned_data['eosinofilos_valor']
    basofilos = form.cleaned_data['basofilos']
    basofilos_valor = form.cleaned_data['basofilos_valor']
    c_plaquetas = form.cleaned_data['c_plaquetas']
    c_plaquetas_valor = form.cleaned_data['c_plaquetas_valor']
    eritro = form.cleaned_data['eritro']
    eritro_valor = form.cleaned_data['eritro_valor']
    fecha_quimica_sanguinea = form.cleaned_data['fecha_quimica_sanguinea']
    creatinina = form.cleaned_data['creatinina']
    creatinina_valor = form.cleaned_data['creatinina_valor']
    tgo = form.cleaned_data['tgo']
    tgo_valor = form.cleaned_data['tgo_valor']
    tgp = form.cleaned_data['tgp']
    tgp_valor = form.cleaned_data['tgp_valor']
    glicemia = form.cleaned_data['glicemia']
    glicemia_valor = form.cleaned_data['glicemia_valor']

    if lab_clinico.exists():
        print "updated"
        lab_clinico = lab_clinico[0]
        lab_clinico.no_inclusion = paciente
        lab_clinico.fecha_hematologicos = fecha_hematologicos
        lab_clinico.hemoglobina = hemoglobina
        lab_clinico.hemoglobina_valor = hemoglobina_valor
        lab_clinico.ctl = ctl
        lab_clinico.ctl_valor = ctl_valor
        lab_clinico.neutrofilos = neutrofilos
        lab_clinico.neutrofilos_valor = neutrofilos_valor
        lab_clinico.linfocitos = linfocitos
        lab_clinico.linfocitos_valor = linfocitos_valor
        lab_clinico.monocitos = monocitos
        lab_clinico.monocitos_valor = monocitos_valor
        lab_clinico.eosinofilos = eosinofilos
        lab_clinico.eosinofilos_valor = eosinofilos_valor
        lab_clinico.basofilos = basofilos
        lab_clinico.basofilos_valor = basofilos_valor
        lab_clinico.c_plaquetas = c_plaquetas
        lab_clinico.c_plaquetas_valor = c_plaquetas_valor
        lab_clinico.eritro = eritro
        lab_clinico.eritro_valor = eritro_valor
        lab_clinico.fecha_quimica_sanguinea = fecha_quimica_sanguinea
        lab_clinico.creatinina = creatinina
        lab_clinico.creatinina_valor = creatinina_valor
        lab_clinico.tgo = tgo
        lab_clinico.tgo_valor = tgo_valor
        lab_clinico.tgp = tgp
        lab_clinico.tgp_valor = tgp_valor
        lab_clinico.glicemia = glicemia
        lab_clinico.glicemia_valor = glicemia_valor

        lab_clinico.save()
    else:
        print "created"
        lab_clinico = models.ExamenLabClinico.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                     dia=dia,
                                                                                     fecha_hematologicos=fecha_hematologicos,
                                                                                     hemoglobina=hemoglobina,
                                                                                     hemoglobina_valor=hemoglobina_valor,
                                                                                     ctl=ctl,
                                                                                     ctl_valor=ctl_valor,
                                                                                     neutrofilos=neutrofilos,
                                                                                     neutrofilos_valor=neutrofilos_valor,
                                                                                     linfocitos=linfocitos,
                                                                                     linfocitos_valor=linfocitos_valor,
                                                                                     monocitos=monocitos,
                                                                                     monocitos_valor=monocitos_valor,
                                                                                     eosinofilos=eosinofilos,
                                                                                     eosinofilos_valor=eosinofilos_valor,
                                                                                     basofilos=basofilos,
                                                                                     basofilos_valor=basofilos_valor,
                                                                                     c_plaquetas=c_plaquetas,
                                                                                     c_plaquetas_valor=c_plaquetas_valor,
                                                                                     eritro=eritro,
                                                                                     eritro_valor=eritro_valor,
                                                                                     fecha_quimica_sanguinea=fecha_quimica_sanguinea,
                                                                                     creatinina=creatinina,
                                                                                     creatinina_valor=creatinina_valor,
                                                                                     tgo=tgo,
                                                                                     tgo_valor=tgo_valor,
                                                                                     tgp=tgp,
                                                                                     tgp_valor=tgp_valor,
                                                                                     glicemia=glicemia,
                                                                                     glicemia_valor=glicemia_valor)
        lab_clinico.save()


@login_required
def view_evaluacion_durante(request, no_inc, dia):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    exist = True
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = 0

    try:
        durante_eval = models.EvaluacionDurante.objects.using(usuario_database).get(no_inclusion=no_inc, dia=dia)
    except ObjectDoesNotExist:
        exist = False
        result = "Evaluacion durante del dia " + dia + " del paciente " + paciente.iniciales
        print "Error"

    examen_fisico = models.ExamenFisico.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=dia)

    mani_clinicas = models.ManifestacionesClinicas.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                          dia=dia)

    otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using(usuario_database).filter(
        no_inclusion__no_inclusion=no_inc,
        dia=dia
    )

    if request.POST:
        form = forms.EvaluacionDuranteForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            update_datos_generales_evaluacion_durante(form=form, exist=exist, durante_eval=durante_eval,
                                                      paciente=paciente, dia=dia, usuario_database=usuario_database)

            update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=dia,
                                 usuario_database=usuario_database)
            result = 1
            return render(request, "eval_durante.html",
                          {'form': form, 'form2': form2, 'form3': form3, 'result': result, 'inc': no_inc, "dia": dia,
                           'paciente': paciente})
        else:
            result = 2

    else:
        if exist:
            i_data = {'fecha': durante_eval.fecha,
                      'previo_diastolica': durante_eval.previo_diastolica,
                      'previo_sistolica': durante_eval.previo_sistolica,
                      'previo_fc': durante_eval.previo_fc,
                      'previo_temperatura': durante_eval.previo_temperatura,
                      'despues_diastolica': durante_eval.despues_diastolica,
                      'despues_sistolica': durante_eval.despues_sistolica,
                      'despues_fc': durante_eval.despues_fc,
                      'despues_temperatura': durante_eval.despues_temperatura,
                      'glicemia_valor': durante_eval.glicemia_valor,
                      'glicemia': durante_eval.glicemia,
                      'fecha_glicemia': durante_eval.fecha_glicemia,
                      'manifestaciones_clinicas': durante_eval.manifestaciones_clinicas,
                      'tratamiento_concomitante': durante_eval.tratamiento_concomitante,
                      'eventos_adversos': durante_eval.eventos_adversos,
                      'interrumpio_tratamiento': durante_eval.interrumpio_tratamiento
                      }
            form = forms.EvaluacionDuranteForm(initial=i_data)
        else:
            form = forms.EvaluacionDuranteForm()

        if examen_fisico.exists():
            examen_fisico = examen_fisico[0]

            i_data = {'peso': examen_fisico.peso,
                      'cv': examen_fisico.cv,
                      'cv_desc': examen_fisico.cv_desc,
                      'respiratorio': examen_fisico.respiratorio,
                      'respiratorio_desc': examen_fisico.respiratorio_desc,
                      'abdominal': examen_fisico.abdominal,
                      'abdominal_desc': examen_fisico.abdominal_desc,
                      'extremidades': examen_fisico.extremidades,
                      'extremidades_desc': examen_fisico.extremidades_desc,
                      'piel': examen_fisico.piel,
                      'piel_desc': examen_fisico.piel_desc,
                      'neurologico': examen_fisico.neurologico,
                      'neurologico_desc': examen_fisico.neurologico_desc
                      }

            form2 = forms.ExamenFisicoForm(initial=i_data)
        else:
            form2 = forms.ExamenFisicoForm()

        if mani_clinicas.exists():
            mani_clinicas = mani_clinicas[0]

            i_data = {'induracion': mani_clinicas.induracion,
                      'edema_local': mani_clinicas.edema_local,
                      'eritema_diametro': mani_clinicas.eritema_diametro,
                      'sensibilidad': mani_clinicas.sensibilidad,
                      'dolor_local': mani_clinicas.dolor_local,
                      'calor_local': mani_clinicas.calor_local,
                      'secrecion_purulenta': mani_clinicas.secrecion_purulenta,
                      'secrecion_no_purulenta': mani_clinicas.secrecion_no_purulenta}

            form3 = forms.ManifestacionesClinicasForm(initial=i_data)
        else:
            form3 = forms.ManifestacionesClinicasForm()

    return render(request, "eval_durante.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'result': result, 'inc': no_inc, "dia": dia,
                   'paciente': paciente})


def update_datos_generales_evaluacion_durante(form, exist, durante_eval, paciente, dia, usuario_database):
    no_inclusion = paciente
    fecha = form.cleaned_data['fecha']
    previo_diastolica = form.cleaned_data['previo_diastolica']
    previo_sistolica = form.cleaned_data['previo_sistolica']
    previo_fc = form.cleaned_data['previo_fc']
    previo_temperatura = form.cleaned_data['previo_temperatura']
    despues_diastolica = form.cleaned_data['despues_diastolica']
    despues_sistolica = form.cleaned_data['despues_sistolica']
    despues_fc = form.cleaned_data['despues_fc']
    despues_temperatura = form.cleaned_data['despues_temperatura']
    glicemia_valor = form.cleaned_data['glicemia_valor']
    glicemia = form.cleaned_data['glicemia']
    fecha_glicemia = form.cleaned_data['fecha_glicemia']
    manifestaciones_clinicas = form.cleaned_data['manifestaciones_clinicas']
    tratamiento_concomitante = form.cleaned_data['tratamiento_concomitante']
    eventos_adversos = form.cleaned_data['eventos_adversos']
    interrumpio_tratamiento = form.cleaned_data['interrumpio_tratamiento']

    if exist:
        print "updated"
        durante_eval.no_inclusion = no_inclusion
        durante_eval.dia = dia
        durante_eval.fecha = fecha
        durante_eval.previo_diastolica = previo_diastolica
        durante_eval.previo_sistolica = previo_sistolica
        durante_eval.previo_fc = previo_fc
        durante_eval.previo_temperatura = previo_temperatura
        durante_eval.despues_diastolica = despues_diastolica
        durante_eval.despues_sistolica = despues_sistolica
        durante_eval.despues_fc = despues_fc
        durante_eval.despues_temperatura = despues_temperatura
        durante_eval.glicemia_valor = glicemia_valor
        durante_eval.glicemia = glicemia
        durante_eval.fecha_glicemia = fecha_glicemia
        durante_eval.manifestaciones_clinicas = manifestaciones_clinicas
        durante_eval.tratamiento_concomitante = tratamiento_concomitante
        durante_eval.eventos_adversos = eventos_adversos
        durante_eval.interrumpio_tratamiento = interrumpio_tratamiento

        durante_eval.save()
    else:
        print "created"
        durante_eval = models.EvaluacionDurante.objects.using(usuario_database).create(no_inclusion=no_inclusion,
                                                                                       dia=dia,
                                                                                       fecha=fecha,
                                                                                       previo_diastolica=previo_diastolica,
                                                                                       previo_sistolica=previo_sistolica,
                                                                                       previo_fc=previo_fc,
                                                                                       previo_temperatura=previo_temperatura,
                                                                                       despues_diastolica=despues_diastolica,
                                                                                       despues_sistolica=despues_sistolica,
                                                                                       despues_fc=despues_fc,
                                                                                       despues_temperatura=despues_temperatura,
                                                                                       glicemia_valor=glicemia_valor,
                                                                                       glicemia=glicemia,
                                                                                       fecha_glicemia=fecha_glicemia,
                                                                                       manifestaciones_clinicas=manifestaciones_clinicas,
                                                                                       tratamiento_concomitante=tratamiento_concomitante,
                                                                                       eventos_adversos=eventos_adversos,
                                                                                       interrumpio_tratamiento=interrumpio_tratamiento
                                                                                       )
        durante_eval.save()


@login_required
def view_evaluacion_final(request, no_inc):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    exist = True
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = 0

    try:
        final_eval = models.EvaluacionFinal.objects.using(usuario_database).get(no_inclusion__no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion final del paciente " + paciente.iniciales
        # print "Error"

    examen_fisico = models.ExamenFisico.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=8)
    eval_micro = models.EvaluacionMicrobiologica.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                        dia=8
                                                                                        )
    lab_clinico = models.ExamenLabClinico.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=8)

    mani_clinicas = models.ManifestacionesClinicas.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                          dia=8)

    otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using(usuario_database).filter(
        no_inclusion__no_inclusion=no_inc,
        dia=8
    )

    germenes = models.RelacionPacienteGermen.objects.using(usuario_database).filter(no_inclusion=no_inc, dia=8)

    if request.POST:
        form = forms.EvaluacionFinalForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        form4 = forms.EvaluacionMicrobiologicaForm(request.POST)
        form5 = forms.ExamenLabClinicoForm(request.POST)
        form6 = forms.ManifestacionesClinicasOtrasForm(request.POST)
        form7 = forms.GermenForm(request.POST)

        form6.no_inc = no_inc
        form6.dia = 8
        form6.user = user

        form7.no_inc = no_inc
        form7.dia = 8
        form7.user = user

        if "nombre_mani_fin" in request.POST:
            nombre = request.POST['nombre_mani_fin']
            try:
                mani = models.RelacionPacManiClinOtras.objects.using(usuario_database).get(no_inclusion=no_inc, dia=8,
                                                                                           nombre=nombre)
                mani.delete()
                context = {'status': 'True', 'nombre': nombre}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")

        else:
            if "nombre_ger_fin" in request.POST:
                nombre = request.POST['nombre_ger_fin']
                try:
                    germen = models.RelacionPacienteGermen.objects.using(usuario_database).get(no_inclusion=no_inc,
                                                                                               dia=8,
                                                                                               nombre=nombre)
                    germen.delete()
                    context = {'status': 'True', 'nombre': nombre}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
                except:
                    context = {'status': 'False'}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
            else:
                if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid() and form7.is_valid():
                    update_datos_generales_evaluacion_final(form=form, exist=exist, final_eval=final_eval,
                                                            paciente=paciente,
                                                            usuario_database=usuario_database)
                    update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=8,
                                         usuario_database=usuario_database)
                    update_manifestaciones_clinicas(form=form3, mani_clinicas=mani_clinicas, paciente=paciente, dia=8,
                                                    usuario_database=usuario_database)

                    update_evaluacion_microbiologica(form=form4, eval_micro=eval_micro, paciente=paciente, dia=8,
                                                     usuario_database=usuario_database)
                    update_examen_lab_clinico(form=form5, lab_clinico=lab_clinico, paciente=paciente, dia=8,
                                              usuario_database=usuario_database)

                    update_otras_manifestaciones_clinicas(form=form6, paciente=paciente, dia=8,
                                                          usuario_database=usuario_database)
                    update_germenes(form=form7, paciente=paciente, dia=8, usuario_database=usuario_database)

                    result = 1
                    return render(request, "eval_final.html",
                                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5,
                                   'form6': form6, 'form7': form7, 'result': result, 'inc': no_inc,
                                   'otras_mani': otras_manifestaciones, 'paciente': paciente,
                                   'germenes': germenes})
                else:
                    result = 2

    else:
        if exist:
            i_data = {'fecha': final_eval.fecha,
                      'manifestaciones_clinicas': final_eval.manifestaciones_clinicas,
                      'cultivo_microbiologico': final_eval.cultivo_microbiologico,
                      'clasificacion_idsa': final_eval.clasificacion_idsa,
                      }
            form = forms.EvaluacionFinalForm(initial=i_data)
        else:
            form = forms.EvaluacionFinalForm()

        if examen_fisico.exists():
            examen_fisico = examen_fisico[0]

            i_data = {'peso': examen_fisico.peso,
                      'cv': examen_fisico.cv,
                      'cv_desc': examen_fisico.cv_desc,
                      'respiratorio': examen_fisico.respiratorio,
                      'respiratorio_desc': examen_fisico.respiratorio_desc,
                      'abdominal': examen_fisico.abdominal,
                      'abdominal_desc': examen_fisico.abdominal_desc,
                      'extremidades': examen_fisico.extremidades,
                      'extremidades_desc': examen_fisico.extremidades_desc,
                      'piel': examen_fisico.piel,
                      'piel_desc': examen_fisico.piel_desc,
                      'neurologico': examen_fisico.neurologico,
                      'neurologico_desc': examen_fisico.neurologico_desc
                      }

            form2 = forms.ExamenFisicoForm(initial=i_data)
        else:
            form2 = forms.ExamenFisicoForm()

        if mani_clinicas.exists():
            mani_clinicas = mani_clinicas[0]

            i_data = {'induracion': mani_clinicas.induracion,
                      'edema_local': mani_clinicas.edema_local,
                      'eritema_diametro': mani_clinicas.eritema_diametro,
                      'sensibilidad': mani_clinicas.sensibilidad,
                      'dolor_local': mani_clinicas.dolor_local,
                      'calor_local': mani_clinicas.calor_local,
                      'secrecion_purulenta': mani_clinicas.secrecion_purulenta,
                      'secrecion_no_purulenta': mani_clinicas.secrecion_no_purulenta}

            form3 = forms.ManifestacionesClinicasForm(initial=i_data)
        else:
            form3 = forms.ManifestacionesClinicasForm()

        if eval_micro.exists():
            eval_micro = eval_micro[0]

            i_data = {'fecha': eval_micro.fecha,
                      'resultado': eval_micro.resultado}

            form4 = forms.EvaluacionMicrobiologicaForm(initial=i_data)
        else:
            form4 = forms.EvaluacionMicrobiologicaForm()

        if lab_clinico.exists():
            lab_clinico = lab_clinico[0]

            i_data = {'fecha_hematologicos': lab_clinico.fecha_hematologicos,
                      'hemoglobina': lab_clinico.hemoglobina,
                      'hemoglobina_valor': lab_clinico.hemoglobina_valor,
                      'ctl': lab_clinico.ctl,
                      'ctl_valor': lab_clinico.ctl_valor,
                      'neutrofilos': lab_clinico.neutrofilos,
                      'neutrofilos_valor': lab_clinico.neutrofilos_valor,
                      'linfocitos': lab_clinico.linfocitos,
                      'linfocitos_valor': lab_clinico.linfocitos_valor,
                      'monocitos': lab_clinico.monocitos,
                      'monocitos_valor': lab_clinico.monocitos_valor,
                      'eosinofilos': lab_clinico.eosinofilos,
                      'eosinofilos_valor': lab_clinico.eosinofilos_valor,
                      'basofilos': lab_clinico.basofilos,
                      'basofilos_valor': lab_clinico.basofilos_valor,
                      'c_plaquetas': lab_clinico.c_plaquetas,
                      'c_plaquetas_valor': lab_clinico.c_plaquetas_valor,
                      'eritro': lab_clinico.eritro,
                      'eritro_valor': lab_clinico.eritro_valor,
                      'fecha_quimica_sanguinea': lab_clinico.fecha_quimica_sanguinea,
                      'creatinina': lab_clinico.creatinina,
                      'creatinina_valor': lab_clinico.creatinina_valor,
                      'tgo': lab_clinico.tgo,
                      'tgo_valor': lab_clinico.tgo_valor,
                      'tgp': lab_clinico.tgp,
                      'tgp_valor': lab_clinico.tgp_valor,
                      'glicemia': lab_clinico.glicemia,
                      'glicemia_valor': lab_clinico.glicemia_valor
                      }

            form5 = forms.ExamenLabClinicoForm(initial=i_data)
        else:
            form5 = forms.ExamenLabClinicoForm()

        form6 = forms.ManifestacionesClinicasOtrasForm()
        form7 = forms.GermenForm()

    return render(request, "eval_final.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6,
                   'form7': form7, 'result': result, 'inc': no_inc,
                   'otras_mani': otras_manifestaciones, 'paciente': paciente,
                   'germenes': germenes})


def update_datos_generales_evaluacion_final(form, exist, final_eval, paciente, usuario_database):
    no_inclusion = paciente
    fecha = form.cleaned_data['fecha']
    manifestaciones_clinicas = form.cleaned_data['manifestaciones_clinicas']
    cultivo_microbiologico = form.cleaned_data['cultivo_microbiologico']
    clasificacion_idsa = form.cleaned_data['clasificacion_idsa']

    if exist:
        print "updated"
        final_eval.no_inclusion = no_inclusion
        final_eval.fecha = fecha
        final_eval.manifestaciones_clinicas = manifestaciones_clinicas
        final_eval.cultivo_microbiologico = cultivo_microbiologico
        final_eval.clasificacion_idsa = clasificacion_idsa

        final_eval.save()
        # result = "Actualizados datos del paciente " + paciente.iniciales + " exitosamente"
    else:
        print "created"
        final_eval = models.EvaluacionFinal.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                   fecha=fecha,
                                                                                   manifestaciones_clinicas=manifestaciones_clinicas,
                                                                                   cultivo_microbiologico=cultivo_microbiologico,
                                                                                   clasificacion_idsa=clasificacion_idsa
                                                                                   )
        final_eval.save()


@login_required
def view_interrupcion_tratamiento(request, no_inc):
    result = 0
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    exist = True
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    # result = "Modifique los datos de interrupcion del tratamiento del paciente " + paciente.iniciales
    causas_otras = [(c.nombre) for c in models.CausasInterrupcionOtras.objects.using(usuario_database).all()]
    muerte = models.Fallecimiento.objects.using(usuario_database).filter(no_inclusion=no_inc)
    necrosias = models.Necrosia.objects.using(usuario_database).filter(no_inclusion=no_inc)

    try:
        interrup_trata = models.InterrupcionTratamiento.objects.using(usuario_database).get(no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de interrupcion del tratamiento del paciente " + paciente.iniciales

    if request.POST:
        if "nombre_necro" in request.POST:
            nombre = request.POST['nombre_necro']
            try:
                hallazgo = models.Necrosia.objects.using(usuario_database).get(no_inclusion=no_inc, hallazgo=nombre)
                hallazgo.delete()
                context = {'status': 'True', 'nombre': nombre}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
        else:
            form = forms.InterrupcionTratamientoForm(request.POST)
            form2 = forms.CausasInterrupcionOtrasForm(request.POST)
            form3 = forms.FallecimientoForm(request.POST)
            form4 = forms.NecrosiaForm(request.POST)

            form4.no_inc = no_inc
            form4.user = request.user.username

            print "Enter post"
            if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                no_inclusion = paciente
                fecha = form.cleaned_data['fecha']
                dosis_recibidas = form.cleaned_data['dosis_recibidas']
                abandono_voluntario = form.cleaned_data['abandono_voluntario']
                criterios_exclusion = form.cleaned_data['criterios_exclusion']
                eventos_adversos = form.cleaned_data['eventos_adversos']
                aparicion_agravamiento = form.cleaned_data['aparicion_agravamiento']
                fallecimiento = form.cleaned_data['fallecimiento']

                nombre = form2.cleaned_data['nombre']

                fecha_muerte = form3.cleaned_data['fecha']
                causa_clinica = form3.cleaned_data['causa_clinica']
                realizo_necrosia = form3.cleaned_data['realizo_necrosia']

                print "Leido formularios"
                if exist:
                    print "updated"
                    interrup_trata.no_inclusion = no_inclusion
                    interrup_trata.fecha = fecha
                    interrup_trata.dosis_recibidas = dosis_recibidas
                    interrup_trata.abandono_voluntario = abandono_voluntario
                    interrup_trata.criterios_exclusion = criterios_exclusion
                    interrup_trata.eventos_adversos = eventos_adversos
                    interrup_trata.aparicion_agravamiento = aparicion_agravamiento
                    interrup_trata.fallecimiento = fallecimiento

                    interrup_trata.save()
                    exist_rel = True
                    if nombre:
                        if nombre not in causas_otras:
                            otra_causa = models.CausasInterrupcionOtras.objects.using(usuario_database).create(
                                nombre=nombre)
                            otra_causa.save()
                            try:
                                relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).get(
                                    no_inclusion=no_inc)
                            except ObjectDoesNotExist:
                                relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).create(
                                    no_inclusion=paciente,
                                    nombre=otra_causa
                                )
                                relacion.save()
                                exist_rel = False

                            if exist_rel:
                                relacion.no_inclusion = no_inclusion
                                relacion.nombre = otra_causa
                                relacion.save()


                        else:
                            otra_causa = models.CausasInterrupcionOtras.objects.using(usuario_database).get(
                                nombre=nombre)
                            try:
                                relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).get(
                                    no_inclusion=no_inc)
                            except ObjectDoesNotExist:
                                relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).create(
                                    no_inclusion=paciente,
                                    nombre=otra_causa
                                )
                                relacion.save()
                                exist_rel = False

                            if exist_rel:
                                relacion.no_inclusion = no_inclusion
                                relacion.nombre = otra_causa
                                relacion.save()

                    else:
                        try:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).get(
                                no_inclusion=no_inc)
                        except ObjectDoesNotExist:
                            exist_rel = False

                        if exist_rel:
                            relacion.delete()

                            # result = 1
                else:
                    # print "created"
                    interrup_trata = models.InterrupcionTratamiento.objects.using(usuario_database).create(
                        no_inclusion=no_inclusion,
                        fecha=fecha,
                        dosis_recibidas=dosis_recibidas,
                        abandono_voluntario=abandono_voluntario,
                        criterios_exclusion=criterios_exclusion,
                        eventos_adversos=eventos_adversos,
                        aparicion_agravamiento=aparicion_agravamiento,
                        fallecimiento=fallecimiento
                    )
                    interrup_trata.save()

                    if nombre:
                        print "Enter en create nombre exist"
                        if nombre not in causas_otras:
                            otra_causa = models.CausasInterrupcionOtras.objects.using(usuario_database).create(
                                nombre=nombre)
                            otra_causa.save()

                        relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).create(
                            no_inclusion=paciente,
                            nombre=otra_causa
                        )

                        relacion.save()
                    else:
                        otra_causa = models.CausasInterrupcionOtras.objects.using(usuario_database).get(nombre=nombre)
                    relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).create(
                        no_inclusion=paciente,
                        nombre=otra_causa
                    )

                    relacion.save()

                if causa_clinica:
                    if muerte.exists():
                        muerte = muerte[0]
                        muerte.fecha = fecha_muerte
                        muerte.causa_clinica = causa_clinica
                        muerte.realizo_necrosia = realizo_necrosia
                        muerte.save()
                    else:
                        muerte = models.Fallecimiento.objects.using(usuario_database).create(no_inclusion=paciente,
                                                                                             fecha=fecha_muerte,
                                                                                             causa_clinica=causa_clinica,
                                                                                             realizo_necrosia=realizo_necrosia)
                        muerte.save()

                update_necrosia(form=form4, paciente=paciente, usuario_datbase=usuario_database)

                result = 1
                return render(request, "interrup_trata.html",
                              {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result,
                               'inc': no_inclusion.no_inclusion,
                               'paciente': paciente, 'necrosias': necrosias})
            else:
                result = 2

    else:
        if exist:
            i_data = {'fecha': interrup_trata.fecha,
                      'dosis_recibidas': interrup_trata.dosis_recibidas,
                      'abandono_voluntario': interrup_trata.abandono_voluntario,
                      'criterios_exclusion': interrup_trata.criterios_exclusion,
                      'eventos_adversos': interrup_trata.eventos_adversos,
                      'aparicion_agravamiento': interrup_trata.aparicion_agravamiento,
                      'fallecimiento': interrup_trata.fallecimiento,
                      }
            form = forms.InterrupcionTratamientoForm(initial=i_data)

        else:
            form = forms.InterrupcionTratamientoForm()

        relacion = models.RelacionPacCausasInterrupOtras.objects.using(usuario_database).filter(no_inclusion=no_inc)

        if relacion.exists():
            form2 = forms.CausasInterrupcionOtrasForm(initial={'nombre': relacion[0].nombre.nombre})
        else:
            form2 = forms.CausasInterrupcionOtrasForm()

        if muerte.exists():
            muerte = muerte[0]
            i_data = {'fecha': muerte.fecha,
                      'causa_clinica': muerte.causa_clinica,
                      'realizo_necrosia': muerte.realizo_necrosia}

            form3 = forms.FallecimientoForm(initial=i_data)
        else:
            form3 = forms.FallecimientoForm()

        form4 = forms.NecrosiaForm()

    return render(request, "interrup_trata.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc,
                   'paciente': paciente, 'necrosias': necrosias})


def update_necrosia(form, paciente, usuario_datbase):
    hallazgo1 = form.cleaned_data['hallazgo1']
    hallazgo2 = form.cleaned_data['hallazgo2']
    hallazgo3 = form.cleaned_data['hallazgo3']

    if hallazgo1:
        necrosia = models.Necrosia.objects.using(usuario_datbase).create(no_inclusion=paciente, hallazgo=hallazgo1)
        necrosia.save()

    if hallazgo2:
        necrosia = models.Necrosia.objects.using(usuario_datbase).create(no_inclusion=paciente, hallazgo=hallazgo2)
        necrosia.save()

    if hallazgo3:
        necrosia = models.Necrosia.objects.using(usuario_datbase).create(no_inclusion=paciente, hallazgo=hallazgo3)
        necrosia.save()


@login_required
def view_eventos_adversos(request, no_inc):
    result = 0
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    eventos_adversos = models.EventosAdversosPaciente.objects.using(usuario_database).filter(no_inclusion=no_inc)
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)

    if request.POST:
        if "nombre_evento" in request.POST:
            nombre = request.POST['nombre_evento']
            evento = models.EventosAdversosPaciente.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                           nombre=nombre)
            if evento.exists():
                evento = evento[0]
                evento.delete()
                context = {"status": "True", "nombre": nombre}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')
            else:
                context = {'status': "False"}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')

        if "add_evento" in request.POST:
            # paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
            form = forms.EventosAdversosPacienteForm(request.POST)
            form2 = forms.EventoAdversoForm(request.POST)

            form2.no_inclusion = no_inc
            form2.user = request.user.username

            print "Enter post"
            if form.is_valid() and form2.is_valid():
                no_inclusion = paciente
                fecha_inicio = form.cleaned_data['fecha_inicio']
                fecha_fin = form.cleaned_data['fecha_fin']
                duracion_24_horas = form.cleaned_data['duracion_24_horas']
                grado_intensidad = form.cleaned_data['grado_intensidad']
                actitud_farmaco = form.cleaned_data['actitud_farmaco']
                resultado = form.cleaned_data['resultado']
                relacion_causalidad = form.cleaned_data['relacion_causalidad']
                lote_dermofural = form.cleaned_data['lote_dermofural']

                nombre = form2.cleaned_data['nombre']

                nombre_evento = models.EventoAdverso.objects.using(usuario_database).filter(nombre=nombre)
                if nombre_evento.exists():
                    nombre_evento = nombre_evento[0]
                else:
                    nombre_evento = models.EventoAdverso.objects.using(usuario_database).create(nombre=nombre)
                    nombre_evento.save()

                print "created"
                evento_adverso = models.EventosAdversosPaciente.objects.using(usuario_database).create(
                    nombre=nombre_evento,
                    no_inclusion=no_inclusion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    duracion_24_horas=duracion_24_horas,
                    grado_intensidad=grado_intensidad,
                    gravedad=0,
                    actitud_farmaco=actitud_farmaco,
                    resultado=resultado,
                    relacion_causalidad=relacion_causalidad,
                    lote_dermofural=lote_dermofural
                )
                evento_adverso.save()

                result = "Datos agregados satisfactriamente al paciente " + paciente.iniciales
                return HttpResponseRedirect(reverse("Eventos_adversos", args=(no_inc,)))
            else:
                result = 2

                # eventos_adversos=models.EventosAdversosPaciente.objects.using(usuario_database).filter(no_inclusion=no_inc)
    else:
        form = forms.EventosAdversosPacienteForm()
        form2 = forms.EventoAdversoForm()
        form2.user = request.user.username

    return render(request, "eventos_adversos.html",
                  {'eventos_adversos': eventos_adversos, 'inc': no_inc, 'form': form, 'form2': form2,
                   'paciente': paciente, 'result': result})


@login_required
def view_mod_evento_adverso(request, no_inc, evento):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = "Modifique el evento adverso " + evento + " del paciente " + paciente.iniciales
    evento_adverso = models.EventosAdversosPaciente.objects.using(usuario_database).get(no_inclusion=no_inc,
                                                                                        nombre=evento)

    if request.POST:
        form = forms.EventosAdversosPacienteForm(request.POST)

        print "Enter post"
        if form.is_valid():
            # no_inclusion=paciente
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            duracion_24_horas = form.cleaned_data['duracion_24_horas']
            grado_intensidad = form.cleaned_data['grado_intensidad']
            actitud_farmaco = form.cleaned_data['actitud_farmaco']
            resultado = form.cleaned_data['resultado']
            relacion_causalidad = form.cleaned_data['relacion_causalidad']
            lote_dermofural = form.cleaned_data['lote_dermofural']

            print "created"

            evento_adverso.fecha_inicio = fecha_inicio
            evento_adverso.fecha_fin = fecha_fin
            evento_adverso.duracion_24_horas = duracion_24_horas
            evento_adverso.grado_intensidad = grado_intensidad
            evento_adverso.actitud_farmaco = actitud_farmaco
            evento_adverso.resultado = resultado
            evento_adverso.relacion_causalidad = relacion_causalidad
            evento_adverso.lote_dermofural = lote_dermofural
            evento_adverso.save()

            result = "Datos agregados satisfactriamente al paciente " + paciente.iniciales
            # eventos_adversos=models.EventosAdversosPaciente.objects.using(usuario_database).filter(no_inclusion=no_inc)
            return HttpResponseRedirect(reverse("Eventos_adversos", args=(no_inc,)))

    else:
        i_data = {'fecha_inicio': evento_adverso.fecha_inicio,
                  'fecha_fin': evento_adverso.fecha_fin,
                  'duracio_24_horas': evento_adverso.duracion_24_horas,
                  'grado_intensidad': evento_adverso.grado_intensidad,
                  'actitud_farmaco': evento_adverso.actitud_farmaco,
                  'resultado': evento_adverso.resultado,
                  'relacion_causalidad': evento_adverso.relacion_causalidad,
                  'evento_adverso': evento_adverso.lote_dermofural,
                  'lote_dermofural': evento_adverso.lote_dermofural,
                  }
        form = forms.EventosAdversosPacienteForm(initial=i_data)

    return render(request, "evento_adverso_mod.html",
                  {'form': form, 'result': result, 'inc': no_inc, 'paciente': paciente})


@login_required
def view_tratamientos_concomitantes(request, no_inc):
    result = 0
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    tratamientos_concomitantes = models.TratamientoConcomitante.objects.using(usuario_database).filter(
        no_inclusion=no_inc)

    if request.POST:
        if "nombre_trata" in request.POST:
            nombre = request.POST['nombre_trata']
            trata = models.TratamientoConcomitante.objects.using(usuario_database).filter(no_inclusion=no_inc,
                                                                                          nombre=nombre)
            if trata.exists():
                trata = trata[0]
                trata.delete()
                context = {"status": "True", "nombre": nombre}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')
            else:
                context = {'status': "False"}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')

        if "add_trata" in request.POST:
            # paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
            form = forms.TratamientoConcomitanteForm(request.POST)
            form2 = forms.MedicamentoForm(request.POST)
            form3 = forms.UnidadForm(request.POST)
            form4 = forms.FrecuenciaForm(request.POST)

            form2.no_inclusion = no_inc
            form2.user = request.user.username

            print "Enter post"
            if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                no_inclusion = paciente
                fecha_inicio = form.cleaned_data['fecha_inicio']
                fecha_fin = form.cleaned_data['fecha_fin']
                duracion_24_horas = form.cleaned_data['duracion_24_horas']
                tratar_eventos_adversos = form.cleaned_data['tratar_eventos_adversos']
                dosis = form.cleaned_data['dosis']

                nombre = form2.cleaned_data['nombre']
                medida = form3.cleaned_data['medida']
                tipo = form4.cleaned_data['tipo']

                nombre_medicamento = models.Medicamento.objects.using(usuario_database).filter(nombre=nombre)
                if nombre_medicamento.exists():
                    nombre_medicamento = nombre_medicamento[0]
                else:
                    nombre_medicamento = models.Medicamento.objects.using(usuario_database).create(nombre=nombre)
                    nombre_medicamento.save()

                unidad_med = models.Unidad.objects.using(usuario_database).filter(medida=medida)
                if unidad_med.exists():
                    unidad_med = unidad_med[0]
                else:
                    unidad_med = models.Unidad.objects.using(usuario_database).create(medida=medida)
                    unidad_med.save()

                tipo_frec = models.Frecuencia.objects.using(usuario_database).filter(tipo=tipo)
                if tipo_frec.exists():
                    tipo_frec = tipo_frec[0]
                else:
                    tipo_frec = models.Frecuencia.objects.using(usuario_database).create(tipo=tipo)
                    tipo_frec.save()

                print "created"
                tratamiento_concomitante = models.TratamientoConcomitante.objects.using(usuario_database).create(
                    nombre=nombre_medicamento,
                    no_inclusion=no_inclusion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    duracion_24_horas=duracion_24_horas,
                    dosis=dosis,
                    tratar_eventos_adversos=tratar_eventos_adversos,
                    medida=unidad_med,
                    tipo=tipo_frec
                )
                tratamiento_concomitante.save()

                return HttpResponseRedirect(reverse("Tratamientos_concomitantes", args=(no_inc,)))
            else:
                result = 2

    else:
        form = forms.TratamientoConcomitanteForm()
        form2 = forms.MedicamentoForm()
        form3 = forms.UnidadForm()
        form4 = forms.FrecuenciaForm()

    return render(request, "tratamientos_con.html",
                  {'tratamientos_concomitantes': tratamientos_concomitantes, 'result': result,
                   'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'inc': no_inc, 'paciente': paciente})


@login_required
def view_mod_tratamiento_concomitante(request, no_inc, trata):
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    paciente = models.Paciente.objects.using(usuario_database).get(no_inclusion=no_inc)
    result = "Modifique el tratamiento concomitante " + trata + " del paciente " + paciente.iniciales
    trata_con = models.TratamientoConcomitante.objects.using(usuario_database).get(no_inclusion=no_inc, nombre=trata)

    if request.POST:
        form = forms.TratamientoConcomitanteForm(request.POST)
        form3 = forms.UnidadForm(request.POST)
        form4 = forms.FrecuenciaForm(request.POST)

        print "Enter post"
        if form.is_valid() and form3.is_valid() and form4.is_valid():
            # no_inclusion=paciente
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            duracion_24_horas = form.cleaned_data['duracion_24_horas']
            tratar_eventos_adversos = form.cleaned_data['tratar_eventos_adversos']
            dosis = form.cleaned_data['dosis']

            medida = form3.cleaned_data['medida']
            tipo = form4.cleaned_data['tipo']

            print "created"

            trata_con.fecha_inicio = fecha_inicio
            trata_con.fecha_fin = fecha_fin
            trata_con.duracion_24_horas = duracion_24_horas
            trata_con.tratar_eventos_adversos = tratar_eventos_adversos
            trata_con.dosis = dosis

            unidad_med = models.Unidad.objects.using(usuario_database).filter(medida=medida)
            if unidad_med.exists():
                unidad_med = unidad_med[0]
            else:
                unidad_med = models.Unidad.objects.using(usuario_database).create(medida=medida)
                unidad_med.save()

            tipo_frec = models.Frecuencia.objects.using(usuario_database).filter(tipo=tipo)
            if tipo_frec.exists():
                tipo_frec = tipo_frec[0]
            else:
                tipo_frec = models.Frecuencia.objects.using(usuario_database).create(tipo=tipo)
                tipo_frec.save()

            trata_con.medida = unidad_med
            trata_con.tipo = tipo_frec
            trata_con.save()

            # result = "Datos agregados satisfactoriamente al paciente " + paciente.iniciales
            # eventos_adversos=models.EventosAdversosPaciente.objects.using(usuario_database).filter(no_inclusion=no_inc)
            return HttpResponseRedirect(reverse("Tratamientos_concomitantes", args=(no_inc,)))

    else:
        i_data = {'fecha_inicio': trata_con.fecha_inicio,
                  'fecha_fin': trata_con.fecha_fin,
                  'duracio_24_horas': trata_con.duracion_24_horas,
                  'tratar_eventos_adversos': trata_con.tratar_eventos_adversos,
                  'dosis': trata_con.dosis,
                  }
        form = forms.TratamientoConcomitanteForm(initial=i_data)

        form3 = forms.UnidadForm(initial={'medida': trata_con.medida.medida})
        form4 = forms.FrecuenciaForm(initial={'tipo': trata_con.tipo.tipo})

    return render(request, "tratamiento_con_mod.html",
                  {'form': form, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc, 'paciente': paciente})


def view_save_csv_report(request):
    # Create the HttpResponse object with the appropriate CSV header.
    user = request.user.username
    usuario_database = UserInfo.objects.using('default').get(user_auth__username__iexact=user).database
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report-' + usuario_database + '.csv"'

    writer = csv.writer(response)
    columns_name = generate_columns_name()
    writer.writerow(columns_name)
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response


def generate_columns_name():
    # Paciente
    result = ['no_inclusion', 'fecha_inc', 'edad', 'sexo', 'raza', 'iniciales']
    # Evaluacion inicial
    result += ['fecha_ini', 'hipertension_arterial', 'hiperlipidemias', 'cardiopatia_isquemica',
               ' historia_ulcera_pies',
               'historia_amputacion', 'amputacion_mayor', 'amputacion_menor', 'tipo_diabetes', 'tiempo_evolucion',
               'habito_fumar', 'alcoholismo', 'miembro_afectado', 'dedos', 'dorso_pie', 'planta', 'calcaneo',
               'lateral_interno', 'lateral_externo', 'transmetatarsiano', 'clasificacion_idsa',
               'cultivo_microbiologico',
               'tratamiento_concomitante']
    # Examen fisico
    # columns_exa_fisico=[]

    return result
