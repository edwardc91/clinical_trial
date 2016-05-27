__author__ = 'root'
from django.shortcuts import render, render_to_response
from django.core.exceptions import ObjectDoesNotExist

import models
import forms


def view_index(request):
    return render(request, 'index.html',list_pacientes())

def view_tests(request):
   frecuencias=[(f.tipo) for f in models.Frecuencia.objects.using('postgredb1').all()]
   medidas=[(u.medida) for u in models.Unidad.objects.using('postgredb1').all()]
   if request.POST:

        form = forms.FrecuenciaForm(request.POST, data_list=frecuencias,prefix="Frecuencia")#PacienteForm(request.POST)
        formM = forms.UnidadForm(request.POST, data_list=medidas,prefix="Medida")
        if form.is_valid() and formM.is_valid():
            return render(request, 'tests.html', {'paciente_form': form, 'unidad_form': formM})
   else:
       form = forms.FrecuenciaForm(data_list=frecuencias, prefix="Frecuencia")#PacienteForm()
       formM = forms.UnidadForm(data_list=medidas, prefix="Medida")

   return render(request, 'tests.html', {'paciente_form' : form, 'unidad_form' : formM})

def list_pacientes():
    pacientes = models.Paciente.objects.using("postgredb1").all().order_by('iniciales')
    context={'pacientes': pacientes}
    return context

def view_paciente(request):
    result="Datos del paciente"
    if request.POST:
        form=forms.PacienteForm(request.POST)
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
            result="Introducidos los datos del paciente "+paciente.iniciales+" exitosamente"
            return render(request, 'paciente.html', {'paciente_form' : form, 'inc' : no_inclusion, 'result': result})
    else:
        form = forms.PacienteForm()
    return render(request, 'paciente.html', {'paciente_form' : form, 'new' : True, 'result': result})

def view_mod_paciente(request,no_inc):
    paciente = models.Paciente.objects.using('postgredb1').get(no_inclusion = no_inc)
    result="Modificar datos del paciente "+paciente.iniciales
    if request.POST:
        form=forms.PacienteForm(request.POST)
        if form.is_valid():
            iniciales = form.cleaned_data["iniciales"]
            no_inclusion = form.cleaned_data["no_inclusion"]
            fecha_inclusion = form.cleaned_data["fecha_inclusion"]
            edad = form.cleaned_data["edad"]
            sexo = form.cleaned_data["sexo"]
            raza = form.cleaned_data['raza']

            paciente.iniciales=iniciales
            paciente.no_inclusion=no_inclusion
            paciente.fecha_inclusion=fecha_inclusion
            paciente.edad=edad
            paciente.sexo=sexo
            paciente.raza=raza

            paciente.save()
            """if no_inc != no_inclusion:
                paciente_old=Paciente.objects.using("postgredb1").filter(no_inclusion=no_inc)
                paciente_old.delete()"""

            result="Actualizados datos del paciente "+paciente.iniciales+" exitosamente"
            return render(request, 'paciente.html', {'paciente_form' : form, 'new' : False, 'inc' : no_inclusion, 'result': result})

    else:
        paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion = no_inc)
        p_data={'no_inclusion': paciente.no_inclusion,
                'fecha_inclusion' : paciente.fecha_inclusion,
                'edad' : paciente.edad,
                'sexo' : paciente.sexo,
                'raza' : paciente.raza,
                'iniciales' : paciente.iniciales}
        form = forms.PacienteForm(initial=p_data)
    return render(request, 'paciente.html', {'paciente_form' : form,'new' : False,'inc' : paciente.no_inclusion, 'result': result})

def view_evaluacion_inicial(request,no_inc):
    exist=True
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Evaluacion inicial del paciente "+paciente.iniciales
    try:
        init_eval = models.EvaluacionInicial.objects.using('postgredb1').get(no_inclusion = no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion inicial del paciente "+paciente.iniciales
        print "Error"

    if request.POST:
        form=forms.EvaluacionInicialForm(request.POST)
        if form.is_valid():
            no_inclusion=paciente
            fecha=form.cleaned_data['fecha']
            hipertension_arterial=form.cleaned_data['hipertension_arterial']
            hiperlipidemias=form.cleaned_data['hiperlipidemias']
            cardiopatia_isquemica=form.cleaned_data['cardiopatia_isquemica']
            historia_ulcera_pies=form.cleaned_data['historia_ulcera_pies']
            historia_amputacion=form.cleaned_data['historia_amputacion']
            amputacion_mayor=form.cleaned_data['amputacion_mayor']
            amputacion_menor=form.cleaned_data['amputacion_menor']
            tipo_diabetes=form.cleaned_data['tipo_diabetes']
            tiempo_evolucion=form.cleaned_data['tiempo_evolucion']
            habito_fumar=form.cleaned_data['habito_fumar']
            alcoholismo=form.cleaned_data['alcoholismo']
            miembro_afectado=form.cleaned_data['miembro_afectado']
            dedos=form.cleaned_data['dedos']
            dorso_pie=form.cleaned_data['dorso_pie']
            planta=form.cleaned_data['planta']
            calcaneo=form.cleaned_data['calcaneo']
            lateral_interno=form.cleaned_data['lateral_interno']
            lateral_externo=form.cleaned_data['lateral_externo']
            transmetatarsiano=form.cleaned_data['transmetatarsiano']
            clasificacion_idsa=form.cleaned_data['clasificacion_idsa']
            cultivo_microbiologico=form.cleaned_data['cultivo_microbiologico']
            tratamiento_concomitante=form.cleaned_data['tratamiento_concomitante']

            if exist:
                print "updated"
                init_eval.no_inclusion=paciente
                init_eval.fecha=fecha
                init_eval.hipertension_arterial=hipertension_arterial
                init_eval.hiperlipidemias=hiperlipidemias
                init_eval.cardiopatia_isquemica=cardiopatia_isquemica
                init_eval.historia_ulcera_pies=historia_ulcera_pies
                init_eval.historia_amputacion=historia_amputacion
                init_eval.amputacion_mayor=amputacion_mayor
                init_eval.amputacion_menor=amputacion_menor
                init_eval.tipo_diabetes=tipo_diabetes
                init_eval.tiempo_evolucion=tiempo_evolucion
                init_eval.habito_fumar=habito_fumar
                init_eval.alcoholismo=alcoholismo
                init_eval.miembro_afectado=miembro_afectado
                init_eval.dedos=dedos
                init_eval.dorso_pie=dorso_pie
                init_eval.planta=planta
                init_eval.calcaneo=calcaneo
                init_eval.lateral_interno=lateral_interno
                init_eval.lateral_externo=lateral_externo
                init_eval.transmetatarsiano=transmetatarsiano
                init_eval.clasificacion_idsa=clasificacion_idsa
                init_eval.cultivo_microbiologico=cultivo_microbiologico
                init_eval.tratamiento_concomitante=tratamiento_concomitante

                init_eval.save()
                result = "Actualizados datos del paciente "+paciente.iniciales+" exitosamente"
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
                result = "Introducidos los datos del paciente "+paciente.iniciales+" exitosamente"
                return render(request, "eval_inicial.html", {'form': form, 'result': result, 'inc': no_inclusion})
    if exist:
        i_data={'fecha': init_eval.fecha,
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
        form=forms.EvaluacionInicialForm(initial=i_data)
    else:
        form=forms.EvaluacionInicialForm()

    return render(request, "eval_inicial.html", {'form': form, 'result': result, 'inc': no_inc})

def view_evaluacion_durante(request, no_inc, dia):
    exist=True
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Evaluacion durante del dia "+dia+" del paciente "+paciente.iniciales

    try:
        durante_eval = models.EvaluacionDurante.objects.using("postgredb1").get(no_inclusion=no_inc, dia=dia)
    except ObjectDoesNotExist:
        exist = False
        result = "Evaluacion durante del dia "+dia+" del paciente "+paciente.iniciales
        print "Error"

    if request.POST:
        form=forms.EvaluacionDuranteForm(request.POST)
        if form.is_valid():
            no_inclusion=paciente
            fecha=form.cleaned_data['fecha']
            previo_diastolica=form.cleaned_data['previo_diastolica']
            previo_sistolica=form.cleaned_data['previo_sistolica']
            previo_fc=form.cleaned_data['previo_fc']
            previo_temperatura=form.cleaned_data['previo_temperatura']
            despues_diastolica=form.cleaned_data['despues_diastolica']
            despues_sistolica=form.cleaned_data['despues_sistolica']
            despues_fc=form.cleaned_data['despues_fc']
            despues_temperatura=form.cleaned_data['despues_temperatura']
            glicemia_valor=form.cleaned_data['glicemia_valor']
            glicemia=form.cleaned_data['glicemia']
            fecha_glicemia=form.cleaned_data['fecha_glicemia']
            manifestaciones_clinicas=form.cleaned_data['manifestaciones_clinicas']
            tratamiento_concomitante=form.cleaned_data['tratamiento_concomitante']
            eventos_adversos=form.cleaned_data['eventos_adversos']
            interrumpio_tratamiento=form.cleaned_data['interrumpio_tratamiento']

            if exist:
                print "updated"
                durante_eval.no_inclusion=no_inclusion
                durante_eval.dia=dia
                durante_eval.fecha=fecha
                durante_eval.previo_diastolica=previo_diastolica
                durante_eval.previo_sistolica=previo_sistolica
                durante_eval.previo_fc=previo_fc
                durante_eval.previo_temperatura=previo_temperatura
                durante_eval.despues_diastolica=despues_diastolica
                durante_eval.despues_sistolica=despues_sistolica
                durante_eval.despues_fc=despues_fc
                durante_eval.despues_temperatura=despues_temperatura
                durante_eval.glicemia_valor=glicemia_valor
                durante_eval.glicemia=glicemia
                durante_eval.fecha_glicemia=fecha_glicemia
                durante_eval.manifestaciones_clinicas=manifestaciones_clinicas
                durante_eval.tratamiento_concomitante=tratamiento_concomitante
                durante_eval.eventos_adversos=eventos_adversos
                durante_eval.interrumpio_tratamiento=interrumpio_tratamiento


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
                return render(request, "eval_durante.html", {'form': form, 'result': result, 'inc': no_inclusion.no_inclusion})
    if exist:
        i_data={'fecha': durante_eval.fecha,
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
        form=forms.EvaluacionDuranteForm(initial=i_data)
    else:
        form=forms.EvaluacionDuranteForm()

    return render(request, "eval_durante.html", {'form': form, 'result': result, 'inc': no_inc})

def view_evaluacion_final(request,no_inc):
    exist=True
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique los datos de la evaluacion final del paciente "+paciente.iniciales

    try:
        final_eval = models.EvaluacionFinal.objects.using("postgredb1").get(no_inclusion__no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de la evaluacion final del paciente "+paciente.iniciales
        print "Error"

    if request.POST:
        form=forms.EvaluacionFinalForm(request.POST)
        if form.is_valid():
            no_inclusion=paciente
            fecha=form.cleaned_data['fecha']
            manifestaciones_clinicas=form.cleaned_data['manifestaciones_clinicas']
            cultivo_microbiologico=form.cleaned_data['cultivo_microbiologico']
            clasificacion_idsa=form.cleaned_data['clasificacion_idsa']


            if exist:
                print "updated"
                final_eval.no_inclusion=no_inclusion
                final_eval.fecha=fecha
                final_eval.manifestaciones_clinicas=manifestaciones_clinicas
                final_eval.cultivo_microbiologico=cultivo_microbiologico
                final_eval.clasificacion_idsa=clasificacion_idsa


                final_eval.save()
                result = "Actualizados datos del paciente "+paciente.iniciales+" exitosamente"
            else:
                print "created"
                final_eval = models.EvaluacionFinal.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                 fecha=fecha,
                                                                                 manifestaciones_clinicas=manifestaciones_clinicas,
                                                                                 cultivo_microbiologico=cultivo_microbiologico,
                                                                                 clasificacion_idsa=clasificacion_idsa
                )
                final_eval.save()
                result = "Introducidos los datos del paciente "+paciente.iniciales+" exitosamente"
                return render(request, "eval_final.html", {'form': form, 'result': result, 'inc': no_inclusion.no_inclusion})
    if exist:
        i_data={'fecha': final_eval.fecha,
                'manifestaciones_clinicas': final_eval.manifestaciones_clinicas,
                'cultivo_microbiologico': final_eval.cultivo_microbiologico,
                'clasificacion_idsa': final_eval.clasificacion_idsa,
        }
        form=forms.EvaluacionFinalForm(initial=i_data)
    else:
        form=forms.EvaluacionFinalForm()

    return render(request, "eval_final.html", {'form': form, 'result': result, 'inc': no_inc})

def view_interrupcion_tratamiento(request,no_inc):
    exist=True
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique los datos de interrupcion del tratamiento del paciente "+paciente.iniciales
    causas_otras = [(c.nombre) for c in models.CausasInterrupcionOtras.objects.using('postgredb1').all()]
    try:
        interrup_trata = models.InterrupcionTratamiento.objects.using("postgredb1").get(no_inclusion=no_inc)
    except ObjectDoesNotExist:
        exist = False
        result = "Introduzca los datos de interrupcion del tratamiento del paciente "+paciente.iniciales

    if request.POST:
        form=forms.InterrupcionTratamientoForm(request.POST)
        form2=forms.CausasInterrupcionOtrasForm(request.POST)
        print "Enter post"
        if form.is_valid() and form2.is_valid():
            no_inclusion=paciente
            fecha=form.cleaned_data['fecha']
            dosis_recibidas=form.cleaned_data['dosis_recibidas']
            abandono_voluntario=form.cleaned_data['abandono_voluntario']
            criterios_exclusion=form.cleaned_data['criterios_exclusion']
            eventos_adversos=form.cleaned_data['eventos_adversos']
            aparicion_agravamiento=form.cleaned_data['aparicion_agravamiento']
            fallecimiento=form.cleaned_data['fallecimiento']

            nombre=form2.cleaned_data['nombre']

            print "Leido formularios"
            if exist:
                print "updated"
                interrup_trata.no_inclusion=no_inclusion
                interrup_trata.fecha=fecha
                interrup_trata.dosis_recibidas=dosis_recibidas
                interrup_trata.abandono_voluntario=abandono_voluntario
                interrup_trata.criterios_exclusion=criterios_exclusion
                interrup_trata.eventos_adversos=eventos_adversos
                interrup_trata.aparicion_agravamiento=aparicion_agravamiento
                interrup_trata.fallecimiento=fallecimiento


                interrup_trata.save()
                exist_rel = True
                if nombre:
                    if nombre not in causas_otras:
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').create(nombre=nombre)
                        otra_causa.save()
                        try:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(no_inclusion=no_inc)
                        except ObjectDoesNotExist:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                                                nombre=otra_causa
                                                                                                                )
                            relacion.save()
                            exist_rel=False

                        if exist_rel:
                            relacion.no_inclusion = no_inclusion
                            relacion.nombre = otra_causa
                            relacion.save()


                    else:
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').get(nombre=nombre)
                        try:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(no_inclusion=no_inc)
                        except ObjectDoesNotExist:
                            relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                                                nombre=otra_causa
                                                                                                                )
                            relacion.save()
                            exist_rel=False

                        if exist_rel:
                            relacion.no_inclusion = no_inclusion
                            relacion.nombre = otra_causa
                            relacion.save()

                else:
                     try:
                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').get(no_inclusion=no_inc)
                     except ObjectDoesNotExist:
                        exist_rel=False

                     if exist_rel:
                        relacion.delete()


                result = "Actualizados datos del paciente "+paciente.iniciales+" exitosamente"
            else:
                print "created"
                interrup_trata = models.InterrupcionTratamiento.objects.using('postgredb1').create(no_inclusion=no_inclusion,
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

                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                                      nombre=otra_causa
                                                                                                      )

                        relacion.save()
                    else:
                        otra_causa = models.CausasInterrupcionOtras.objects.using('postgredb1').get(nombre=nombre)
                        relacion = models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').create(no_inclusion=paciente,
                                                                                                      nombre=otra_causa
                                                                                                      )

                        relacion.save()

                result = "Introducidos los datos del paciente "+paciente.iniciales+" exitosamente"
                return render(request, "interrup_trata.html", {'form': form,'form2': form2, 'result': result, 'inc': no_inclusion.no_inclusion})
    if exist:
        i_data={'fecha': interrup_trata.fecha,
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

    relacion=models.RelacionPacCausasInterrupOtras.objects.using('postgredb1').filter(no_inclusion=no_inc)
    if relacion.exists():
        form2=forms.CausasInterrupcionOtrasForm(initial={'nombre': relacion[0].nombre.nombre})
    else:
        form2=forms.CausasInterrupcionOtrasForm()

    return render(request, "interrup_trata.html", {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})

def view_eventos_adversos(request,no_inc):

    eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
    return render(request,"eventos_adversos.html", {'eventos_adversos': eventos_adversos, 'inc': no_inc})

def view_evento_adverso(request,no_inc):
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Nuevo evento adverso"

    if request.POST:
        form=forms.EventosAdversosPacienteForm(request.POST)
        form2=forms.EventoAdversoForm(request.POST)

        form2.no_inclusion=no_inc
        print "Enter post"
        if form.is_valid() and form2.is_valid():
            no_inclusion=paciente
            fecha_inicio=form.cleaned_data['fecha_inicio']
            fecha_fin=form.cleaned_data['fecha_fin']
            duracion_24_horas=form.cleaned_data['duracion_24_horas']
            grado_intensidad=form.cleaned_data['grado_intensidad']
            actitud_farmaco=form.cleaned_data['actitud_farmaco']
            resultado=form.cleaned_data['resultado']
            relacion_causalidad=form.cleaned_data['relacion_causalidad']
            lote_dermofural=form.cleaned_data['lote_dermofural']

            nombre = form2.cleaned_data['nombre']

            nombre_evento = models.EventoAdverso.objects.using('postgredb1').filter(nombre=nombre)
            if nombre_evento.exists():
                nombre_evento=nombre_evento[0]
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

            result="Datos agregados satisfactriamente al paciente "+paciente.iniciales
            #eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "evento_adverso.html", {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})

    form = forms.EventosAdversosPacienteForm()
    form2 = forms.EventoAdversoForm()
    form2.no_inclusion = no_inc

    return render(request, "evento_adverso.html", {'form': form, 'form2': form2, 'result': result, 'inc': no_inc})

def view_mod_evento_adverso(request,no_inc,evento):
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Modifique el evento adverso "+evento+" del paciente "+paciente.iniciales
    evento_adverso = models.EventosAdversosPaciente.objects.using('postgredb1').get(no_inclusion=no_inc,nombre=evento)

    if request.POST:
        form=forms.EventosAdversosPacienteForm(request.POST)

        print "Enter post"
        if form.is_valid():
            #no_inclusion=paciente
            fecha_inicio=form.cleaned_data['fecha_inicio']
            fecha_fin=form.cleaned_data['fecha_fin']
            duracion_24_horas=form.cleaned_data['duracion_24_horas']
            grado_intensidad=form.cleaned_data['grado_intensidad']
            actitud_farmaco=form.cleaned_data['actitud_farmaco']
            resultado=form.cleaned_data['resultado']
            relacion_causalidad=form.cleaned_data['relacion_causalidad']
            lote_dermofural=form.cleaned_data['lote_dermofural']

            print "created"

            evento_adverso.fecha_inicio=fecha_inicio
            evento_adverso.fecha_fin=fecha_fin
            evento_adverso.duracion_24_horas=duracion_24_horas
            evento_adverso.grado_intensidad=grado_intensidad
            evento_adverso.actitud_farmaco=actitud_farmaco
            evento_adverso.resultado=resultado
            evento_adverso.relacion_causalidad=relacion_causalidad
            evento_adverso.lote_dermofural=lote_dermofural
            evento_adverso.save()

            result="Datos agregados satisfactriamente al paciente "+paciente.iniciales
            #eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "mod_evento_adverso.html", {'form': form, 'result': result, 'inc': no_inc})


    i_data={'fecha_inicio': evento_adverso.fecha_inicio,
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

    return render(request, "mod_evento_adverso.html", {'form': form, 'result': result, 'inc': no_inc})

def view_tratamientos_concomitantes(request,no_inc):

    tratamientos_concomitantes=models.TratamientoConcomitante.objects.using('postgredb1').filter(no_inclusion=no_inc)
    return render(request,"tratamientos_con.html", {'tratamientos_concomitantes': tratamientos_concomitantes, 'inc': no_inc})

def view_tratamiento_concomitante(request,no_inc):
    paciente=models.Paciente.objects.using("postgredb1").get(no_inclusion=no_inc)
    result = "Agregue un tratamiento concomitante al paciente "+paciente.iniciales

    if request.POST:
        form=forms.TratamientoConcomitanteForm(request.POST)
        form2=forms.MedicamentoForm(request.POST)
        form3=forms.UnidadForm(request.POST)
        form4=forms.FrecuenciaForm(request.POST)

        form2.no_inclusion=no_inc
        print "Enter post"
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            no_inclusion=paciente
            fecha_inicio=form.cleaned_data['fecha_inicio']
            fecha_fin=form.cleaned_data['fecha_fin']
            duracion_24_horas=form.cleaned_data['duracion_24_horas']
            tratar_eventos_adversos=form.cleaned_data['tratar_eventos_adversos']
            dosis=form.cleaned_data['dosis']

            nombre = form2.cleaned_data['nombre']
            medida=form3.cleaned_data['medida']
            tipo=form4.cleaned_data['tipo']

            nombre_medicamento = models.Medicamento.objects.using('postgredb1').filter(nombre=nombre)
            if nombre_medicamento.exists():
                nombre_medicamento=nombre_medicamento[0]
            else:
                nombre_medicamento = models.Medicamento.objects.using('postgredb1').create(nombre=nombre)
                nombre_medicamento.save()

            unidad_med = models.Unidad.objects.using('postgredb1').filter(medida=medida)
            if unidad_med.exists():
                 unidad_med=unidad_med[0]
            else:
                 unidad_med = models.Unidad.objects.using('postgredb1').create(medida=medida)
                 unidad_med.save()

            tipo_frec = models.Frecuencia.objects.using('postgredb1').filter(tipo=tipo)
            if tipo_frec.exists():
                tipo_frec=tipo_frec[0]
            else:
                tipo_frec = models.Frecuencia.objects.using('postgredb1').create(tipo=tipo)
                tipo_frec.save()

            print "created"
            tratamiento_concomitante = models.TratamientoConcomitante.objects.using('postgredb1').create(nombre=nombre_medicamento,
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

            result="Datos agregados satisfactriamente al paciente "+paciente.iniciales
            #eventos_adversos=models.EventosAdversosPaciente.objects.using('postgredb1').filter(no_inclusion=no_inc)
            return render(request, "tratamiento_con.html", {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc})

    form = forms.TratamientoConcomitanteForm()
    form2 = forms.MedicamentoForm()
    form2.no_inclusion = no_inc

    form3=forms.UnidadForm()
    form4=forms.FrecuenciaForm()

    return render(request, "tratamiento_con.html", {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'result': result, 'inc': no_inc})