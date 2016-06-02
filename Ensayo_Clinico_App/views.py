__author__ = 'root'
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_exempt
import json, simplejson

import models
import forms

@csrf_exempt
def view_evento_delete_ajax(request, no_inc, nombre):
    evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc, nombre=nombre)

    if evento_adverso.exists():
        evento_adverso = evento_adverso[0]
        evento_adverso.delete()

        return HttpResponse(json.dump(nombre), content_type="application/json")





def view_index(request):
    return render(request, 'index.html', list_pacientes())


def view_tests(request):
    frecuencias = [(f.tipo) for f in models.Frecuencia.objects.using('postgredb1').all()]
    medidas = [(u.medida) for u in models.Unidad.objects.using('postgredb1').all()]
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


def list_pacientes():
    pacientes = models.Paciente.objects.using("postgredb1").all().order_by('iniciales')
    context = {'pacientes': pacientes}
    return context


def view_paciente(request):
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

            paciente = models.Paciente.objects.using('postgredb1').create(iniciales=iniciales,
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


def view_mod_paciente(request, no_inc):
    paciente = models.Paciente.objects.using('postgredb1').get(no_inclusion=no_inc)
    result = "Modificar datos del paciente " + paciente.iniciales
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
                paciente_old=Paciente.objects.using("postgredb1").filter(no_inclusion=no_inc)
                paciente_old.delete()"""

            result = "Actualizados datos del paciente " + paciente.iniciales + " exitosamente"
            return render(request, 'paciente_mod.html',
                          {'paciente_form': form, 'inc': no_inclusion, 'result': result})

    else:
        paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
        p_data = {'no_inclusion': paciente.no_inclusion,
                  'fecha_inclusion': paciente.fecha_inclusion,
                  'edad': paciente.edad,
                  'sexo': paciente.sexo,
                  'raza': paciente.raza,
                  'iniciales': paciente.iniciales}
        form = forms.PacienteForm(initial=p_data)
    return render(request, 'paciente_mod.html',
                  {'paciente_form': form, 'inc': paciente.no_inclusion, 'result': result})


def view_evaluacion_inicial(request, no_inc):
    exist = True
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Evaluacion inicial del paciente " + paciente.iniciales
    try:
        init_eval = models.EvaluacionInicial.objects.using('postgredb1').get(no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion inicial del paciente " + paciente.iniciales
        # print "Error"

    examen_fisico = models.ExamenFisico.objects.using('postgredb1').filter(no_inclusion=no_inc, dia=0)
    eval_micro = models.EvaluacionMicrobiologica.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                    dia=0
                                                                                    )
    lab_clinico = models.ExamenLabClinico.objects.using('postgredb1').filter(no_inclusion=no_inc, dia=0)


    mani_clinicas = models.ManifestacionesClinicas.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                      dia=0)

    """otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using('postgredb1').filter(
        no_inclusion__no_inclusion=no_inc,
        dia=0
    )"""

    if request.POST:
        form = forms.EvaluacionInicialForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        form4 = forms.EvaluacionMicrobiologicaForm(request.POST)
        form5 = forms.ExamenLabClinicoForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            update_datos_generales_evaluacion_inicial(form=form, exist=exist, init_eval=init_eval,
                                                      paciente=paciente)
            update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=0)

            print "right here"
            update_manifestaciones_clinicas(form=form3, mani_clinicas=mani_clinicas, paciente=paciente, dia=0)
            update_evaluacion_microbiologica(form=form4, eval_micro=eval_micro, paciente=paciente, dia=0)
            update_examen_lab_clinico(form=form5, lab_clinico=lab_clinico, paciente=paciente, dia=0)

            result = "Modificados los datos de la evaluacion inicial de paciente " + paciente.iniciales + " satisfactoriamente"
            return render(request, "eval_inicial.html",
                          {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5,
                           'result': result, 'inc': no_inc})
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
        mani_clinicas=mani_clinicas[0]
        
        i_data={'induracion': mani_clinicas.induracion,
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

    return render(request, "eval_inicial.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'result': result,
                   'inc': no_inc})


def update_datos_generales_evaluacion_inicial(form, exist, init_eval, paciente):
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
        print "updated"
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
        init_eval = models.EvaluacionInicial.objects.using('postgredb1').create(no_inclusion=paciente,
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


def update_examen_fisico(form, examen_fisico, paciente, dia):
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
        examen_fisico = models.ExamenFisico.objects.using('postgredb1').create(no_inclusion=paciente,
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


def update_manifestaciones_clinicas(form, mani_clinicas, paciente, dia):
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
        mani_clinicas = models.ManifestacionesClinicas.objects.using('postgredb1').create(no_inclusion=paciente,
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


def update_evaluacion_microbiologica(form, eval_micro, paciente, dia):
    fecha = form.cleaned_data['fecha']
    resultado = form.cleaned_data['resultado']

    if eval_micro.exists():
        print "updated"
        eval_micro = eval_micro[0]

        eval_micro.no_inclusion = paciente
        eval_micro.fecha = fecha
        eval_micro.resultado = resultado

        eval_micro.save()
    else:
        print "created"
        eval_micro = models.EvaluacionMicrobiologica.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                        dia=dia,
                                                                                        fecha=fecha,
                                                                                        resultado=resultado
                                                                                        )
        eval_micro.save()


def update_examen_lab_clinico(form, lab_clinico, paciente, dia):
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
        lab_clinico = models.ExamenLabClinico.objects.using('postgredb1').create(no_inclusion=paciente,
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


def view_evaluacion_durante(request, no_inc, dia):
    exist = True
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Evaluacion durante del dia " + dia + " del paciente " + paciente.iniciales

    try:
        durante_eval = models.EvaluacionDurante.objects.using("postgredb1").get(no_inclusion=no_inc, dia=dia)
    except ObjectDoesNotExist:
        exist = False
        result = "Evaluacion durante del dia " + dia + " del paciente " + paciente.iniciales
        print "Error"

    examen_fisico = models.ExamenFisico.objects.using('postgredb1').filter(no_inclusion=no_inc, dia=dia)

    mani_clinicas = models.ManifestacionesClinicas.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                      dia=dia)

    otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using('postgredb1').filter(
        no_inclusion__no_inclusion=no_inc,
        dia=dia
    )

    if request.POST:
        form = forms.EvaluacionDuranteForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            update_datos_generales_evaluacion_durante(form=form, exist=exist, durante_eval=durante_eval,
                                                      paciente=paciente, dia=dia)

            update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=dia)
            return render(request, "eval_durante.html",
                          {'form': form, 'form2': form2, 'form3': form3, 'result': result, 'inc': no_inc,"dia":dia})
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
                  {'form': form, 'form2': form2, 'form3': form3, 'result': result, 'inc': no_inc,"dia":dia})


def update_datos_generales_evaluacion_durante(form, exist, durante_eval, paciente, dia):
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
        durante_eval = models.EvaluacionDurante.objects.using('postgredb1').create(no_inclusion=no_inclusion,
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


def view_evaluacion_final(request, no_inc):
    exist = True
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique los datos de la evaluacion final del paciente " + paciente.iniciales

    try:
        final_eval = models.EvaluacionFinal.objects.using("postgredb1").get(no_inclusion__no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion final del paciente " + paciente.iniciales
        # print "Error"

    examen_fisico = models.ExamenFisico.objects.using('postgredb1').filter(no_inclusion=no_inc, dia=8)
    eval_micro = models.EvaluacionMicrobiologica.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                    dia=8
                                                                                    )
    lab_clinico = models.ExamenLabClinico.objects.using('postgredb1').filter(no_inclusion=no_inc, dia=8)

    mani_clinicas = models.ManifestacionesClinicas.objects.using('postgredb1').filter(no_inclusion=no_inc,
                                                                                      dia=8)

    otras_manifestaciones = models.RelacionPacManiClinOtras.objects.using('postgredb1').filter(
        no_inclusion__no_inclusion=no_inc,
        dia=8
    )

    if request.POST:
        form = forms.EvaluacionFinalForm(request.POST)
        form2 = forms.ExamenFisicoForm(request.POST)
        form3 = forms.ManifestacionesClinicasForm(request.POST)
        form4 = forms.EvaluacionMicrobiologicaForm(request.POST)
        form5 = forms.ExamenLabClinicoForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            update_datos_generales_evaluacion_final(form=form, exist=exist, final_eval=final_eval, paciente=paciente)
            update_examen_fisico(form=form2, examen_fisico=examen_fisico, paciente=paciente, dia=8)

            update_evaluacion_microbiologica(form=form4, eval_micro=eval_micro, paciente=paciente, dia=8)
            update_examen_lab_clinico(form=form5, lab_clinico=lab_clinico, paciente=paciente, dia=8)

            result = "Introducidos los datos del paciente " + paciente.iniciales + " exitosamente"
            return render(request, "eval_final.html",
                          {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5,
                           'result': result, 'inc': no_inc})
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

    return render(request, "eval_final.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'result': result,
                   'otras_mani': otras_manifestaciones, 'inc': no_inc})


def update_datos_generales_evaluacion_final(form, exist, final_eval, paciente):
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
        final_eval = models.EvaluacionFinal.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                               fecha=fecha,
                                                                               manifestaciones_clinicas=manifestaciones_clinicas,
                                                                               cultivo_microbiologico=cultivo_microbiologico,
                                                                               clasificacion_idsa=clasificacion_idsa
                                                                               )
        final_eval.save()


def view_interrupcion_tratamiento(request, no_inc):
    exist = True
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique los datos de interrupcion del tratamiento del paciente " + paciente.iniciales
    causas_otras = [(c.nombre) for c in models.CausasInterrupcionOtras.objects.using('postgredb1').all()]
    try:
        interrup_trata = models.InterrupcionTratamiento.objects.using("postgredb1").get(no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de interrupcion del tratamiento del paciente " + paciente.iniciales

    if request.POST:
        form = forms.InterrupcionTratamientoForm(request.POST)
        form2 = forms.CausasInterrupcionOtrasForm(request.POST)
        print "Enter post"
        if form.is_valid() and form2.is_valid():
            no_inclusion = paciente
            fecha = form.cleaned_data['fecha']
            dosis_recibidas = form.cleaned_data['dosis_recibidas']
            abandono_voluntario = form.cleaned_data['abandono_voluntario']
            criterios_exclusion = form.cleaned_data['criterios_exclusion']
            eventos_adversos = form.cleaned_data['eventos_adversos']
            aparicion_agravamiento = form.cleaned_data['aparicion_agravamiento']
            fallecimiento = form.cleaned_data['fallecimiento']

            nombre = form2.cleaned_data['nombre']

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
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').create(nombre=nombre)
                        otra_causa.save()
                        try:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(
                                no_inclusion=no_inc)
                        except ObjectDoesNotExist:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(
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
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').get(nombre=nombre)
                        try:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(
                                no_inclusion=no_inc)
                        except ObjectDoesNotExist:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(
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
                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(
                            no_inclusion=no_inc)
                    except ObjectDoesNotExist:
                        exist_rel = False

                    if exist_rel:
                        relacion.delete()

                result = "Actualizados datos del paciente " + paciente.iniciales + " exitosamente"
            else:
                print "created"
                interrup_trata = models.InterrupcionTratamiento.objects.using('postgredb1').create(
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
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').create(nombre=nombre)
                        otra_causa.save()

                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(
                            no_inclusion=paciente,
                            nombre=otra_causa
                        )

                        relacion.save()
                    else:
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').get(nombre=nombre)
                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(
                            no_inclusion=paciente,
                            nombre=otra_causa
                        )

                        relacion.save()

                result = "Introducidos los datos del paciente " + paciente.iniciales + " exitosamente"
                return render(request, "interrup_trata.html",
                              {'form': form, 'form2': form2, 'result': result, 'inc': no_inclusion.no_inclusion})
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

    relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').filter(no_inclusion=no_inc)
    if relacion.exists():
        form2 = forms.CausasInterrupcionOtrasForm(initial={'nombre': relacion[0].nombre.nombre})
    else:
        form2 = forms.CausasInterrupcionOtrasForm()

    return render(request, "interrup_trata.html", {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})


def view_eventos_adversos(request, no_inc):
    eventos_adversos = models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)

    if request.POST:
        if "nombre_evento" in request.POST:
            nombre=request.POST['nombre_evento']
            evento=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc,nombre=nombre)
            if evento.exists():
                evento=evento[0]
                evento.delete()
                context = {"status": "True", "nombre": nombre}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')
            else:
                context = {'status': "False"}
                return HttpResponse(simplejson.dumps(context), content_type='application/json')

        if "add_evento" in request.POST:
            paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
            form = forms.EventosAdversosPacienteForm(request.POST)
            form2 = forms.EventoAdversoForm(request.POST)

            form2.no_inclusion = no_inc
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

                nombre_evento = models.EventoAdverso.objects.using('postgredb1').filter(nombre=nombre)
                if nombre_evento.exists():
                    nombre_evento = nombre_evento[0]
                else:
                    nombre_evento = models.EventoAdverso.objects.using('postgredb1').create(nombre=nombre)
                    nombre_evento.save()

                print "created"
                evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').create(nombre=nombre_evento,
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
                return HttpResponseRedirect(reverse("Eventos_adversos",args=(no_inc,)))

            # eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)

    form = forms.EventosAdversosPacienteForm()
    form2 = forms.EventoAdversoForm()

    return render(request, "eventos_adversos.html", {'eventos_adversos': eventos_adversos, 'inc': no_inc,'form': form, 'form2': form2})


def view_evento_adverso(request, no_inc):
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Nuevo evento adverso"

    if request.POST:
        form = forms.EventosAdversosPacienteForm(request.POST)
        form2 = forms.EventoAdversoForm(request.POST)

        form2.no_inclusion = no_inc
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

            nombre_evento = models.EventoAdverso.objects.using('postgredb1').filter(nombre=nombre)
            if nombre_evento.exists():
                nombre_evento = nombre_evento[0]
            else:
                nombre_evento = models.EventoAdverso.objects.using('postgredb1').create(nombre=nombre)
                nombre_evento.save()

            print "created"
            evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').create(nombre=nombre_evento,
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
            # eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "evento_adverso.html",
                          {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})

    form = forms.EventosAdversosPacienteForm()
    form2 = forms.EventoAdversoForm()
    form2.no_inclusion = no_inc

    return render(request, "evento_adverso.html", {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})


def view_mod_evento_adverso(request, no_inc, evento):
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique el evento adverso " + evento + " del paciente " + paciente.iniciales
    evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').get(no_inclusion=no_inc, nombre=evento)

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
            # eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "evento_adverso_mod.html", {'form': form, 'result': result, 'inc': no_inc})

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

    return render(request, "evento_adverso_mod.html", {'form': form, 'result': result, 'inc': no_inc})


def view_tratamientos_concomitantes(request, no_inc):
    tratamientos_concomitantes = models.TratamientoConcomitante.objects.using('postgredb1').filter(no_inclusion=no_inc)
    return render(request, "tratamientos_con.html",
                  {'tratamientos_concomitantes': tratamientos_concomitantes, 'inc': no_inc})


def view_tratamiento_concomitante(request, no_inc):
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Agregue un tratamiento concomitante al paciente " + paciente.iniciales

    if request.POST:
        form = forms.TratamientoConcomitanteForm(request.POST)
        form2 = forms.MedicamentoForm(request.POST)
        form3 = forms.UnidadForm(request.POST)
        form4 = forms.FrecuenciaForm(request.POST)

        form2.no_inclusion = no_inc
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

            nombre_medicamento = models.Medicamento.objects.using('postgredb1').filter(nombre=nombre)
            if nombre_medicamento.exists():
                nombre_medicamento = nombre_medicamento[0]
            else:
                nombre_medicamento = models.Medicamento.objects.using('postgredb1').create(nombre=nombre)
                nombre_medicamento.save()

            unidad_med = models.Unidad.objects.using('postgredb1').filter(medida=medida)
            if unidad_med.exists():
                unidad_med = unidad_med[0]
            else:
                unidad_med = models.Unidad.objects.using('postgredb1').create(medida=medida)
                unidad_med.save()

            tipo_frec = models.Frecuencia.objects.using('postgredb1').filter(tipo=tipo)
            if tipo_frec.exists():
                tipo_frec = tipo_frec[0]
            else:
                tipo_frec = models.Frecuencia.objects.using('postgredb1').create(tipo=tipo)
                tipo_frec.save()

            print "created"
            tratamiento_concomitante = models.TratamientoConcomitante.objects.using('postgredb1').create(
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

            result = "Datos agregados satisfactriamente al paciente " + paciente.iniciales
            # eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "tratamiento_con.html",
                          {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result,
                           'inc': no_inc})

    form = forms.TratamientoConcomitanteForm()
    form2 = forms.MedicamentoForm()
    form2.no_inclusion = no_inc

    form3 = forms.UnidadForm()
    form4 = forms.FrecuenciaForm()

    return render(request, "tratamiento_con.html",
                  {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc})


def view_mod_tratamiento_concomitante(request, no_inc, trata):
    paciente = models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique el tratamiento concomitante " + trata + " del paciente " + paciente.iniciales
    trata_con = models.TratamientoConcomitante.objects.using('postgredb1').get(no_inclusion=no_inc, nombre=trata)

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

            unidad_med = models.Unidad.objects.using('postgredb1').filter(medida=medida)
            if unidad_med.exists():
                unidad_med = unidad_med[0]
            else:
                unidad_med = models.Unidad.objects.using('postgredb1').create(medida=medida)
                unidad_med.save()

            tipo_frec = models.Frecuencia.objects.using('postgredb1').filter(tipo=tipo)
            if tipo_frec.exists():
                tipo_frec = tipo_frec[0]
            else:
                tipo_frec = models.Frecuencia.objects.using('postgredb1').create(tipo=tipo)
                tipo_frec.save()

            trata_con.medida = unidad_med
            trata_con.tipo = tipo_frec
            trata_con.save()

            result = "Datos agregados satisfactoriamente al paciente " + paciente.iniciales
            # eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "tratamiento_con_mod.html",
                          {'form': form, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc})

    i_data = {'fecha_inicio': trata_con.fecha_inicio,
              'fecha_fin': trata_con.fecha_fin,
              'duracio_24_horas': trata_con.duracion_24_horas,
              'tratar_eventos_adversos': trata_con.tratar_eventos_adversos,
              'dosis': trata_con.dosis,
              }
    form = forms.TratamientoConcomitanteForm(initial=i_data)
    # faltan valores iniciales
    form3 = forms.UnidadForm(initial={'medida': trata_con.medida.medida})
    form4 = forms.FrecuenciaForm(initial={'tipo': trata_con.tipo.tipo})

    return render(request, "tratamiento_con_mod.html",
                  {'form': form, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc})
