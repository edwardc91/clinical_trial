# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class CausasInterrupcionOtras(models.Model):
    nombre = models.CharField(primary_key=True, max_length=50)

    class Meta:
        db_table = 'Causas_interrupcion_otras'


class EvaluacionDurante(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    dia = models.SmallIntegerField()
    fecha = models.DateField(blank=True, null=True)
    previo_diastolica = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    previo_sistolica = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    previo_fc = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    previo_temperatura = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    despues_diastolica = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    despues_sistolica = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    despues_fc = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    despues_temperatura = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    glicemia_valor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    glicemia = models.SmallIntegerField(blank=True, null=True)
    fecha_glicemia = models.DateField(blank=True, null=True)
    manifestaciones_clinicas = models.SmallIntegerField(blank=True, null=True)
    tratamiento_concomitante = models.SmallIntegerField(blank=True, null=True)
    eventos_adversos = models.SmallIntegerField(blank=True, null=True)
    interrumpio_tratamiento = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion_durante'
        unique_together = (('no_inclusion', 'dia'),)


class EvaluacionFinal(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    cultivo_microbiologico = models.SmallIntegerField(blank=True, null=True)
    manifestaciones_clinicas = models.SmallIntegerField(blank=True, null=True)
    clasificacion_idsa = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion_final'


class EvaluacionInicial(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    hipertension_arterial = models.SmallIntegerField(blank=True, null=True)
    hiperlipidemias = models.SmallIntegerField(blank=True, null=True)
    cardiopatia_isquemica = models.SmallIntegerField(blank=True, null=True)
    historia_ulcera_pies = models.SmallIntegerField(blank=True, null=True)
    historia_amputacion = models.SmallIntegerField(blank=True, null=True)
    amputacion_mayor = models.SmallIntegerField(blank=True, null=True)
    amputacion_menor = models.SmallIntegerField(blank=True, null=True)
    tipo_diabetes = models.SmallIntegerField(blank=True, null=True)
    tiempo_evolucion = models.SmallIntegerField(blank=True, null=True)
    habito_fumar = models.SmallIntegerField(blank=True, null=True)
    alcoholismo = models.SmallIntegerField(blank=True, null=True)
    miembro_afectado = models.SmallIntegerField(blank=True, null=True)
    dedos = models.SmallIntegerField(blank=True, null=True)
    dorso_pie = models.SmallIntegerField(blank=True, null=True)
    planta = models.SmallIntegerField(blank=True, null=True)
    calcaneo = models.SmallIntegerField(blank=True, null=True)
    lateral_interno = models.SmallIntegerField(blank=True, null=True)
    lateral_externo = models.SmallIntegerField(blank=True, null=True)
    transmetatarsiano = models.SmallIntegerField(blank=True, null=True)
    clasificacion_idsa = models.SmallIntegerField(blank=True, null=True)
    cultivo_microbiologico = models.SmallIntegerField(blank=True, null=True)
    tratamiento_concomitante = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion_inicial'


class EvaluacionMicrobiologica(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    dia = models.SmallIntegerField()
    fecha = models.DateField(blank=True, null=True)
    resultado = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Evaluacion_microbiologica'
        unique_together = (('no_inclusion', 'dia'),)


class EventoAdverso(models.Model):
    nombre = models.CharField(primary_key=True, max_length=50)

    class Meta:
        db_table = 'Evento_adverso'


class EventosAdversosPaciente(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    nombre = models.ForeignKey(EventoAdverso, db_column='nombre')
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    duracion_24_horas = models.TimeField(blank=True, null=True)
    grado_intensidad = models.SmallIntegerField(blank=True, null=True)
    gravedad = models.SmallIntegerField(blank=True, null=True)
    actitud_farmaco = models.SmallIntegerField(blank=True, null=True)
    resultado = models.SmallIntegerField(blank=True, null=True)
    relacion_causalidad = models.SmallIntegerField(blank=True, null=True)
    lote_dermofural = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'Eventos_adversos_paciente'
        unique_together = (('no_inclusion', 'nombre'),)


class ExamenFisico(models.Model):
    dia = models.IntegerField()
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    peso = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    cv = models.SmallIntegerField(blank=True, null=True)
    cv_desc = models.CharField(max_length=50, blank=True, null=True)
    respiratorio = models.SmallIntegerField(blank=True, null=True)
    respiratorio_desc = models.CharField(max_length=50, blank=True, null=True)
    abdominal = models.SmallIntegerField(blank=True, null=True)
    abdominal_desc = models.CharField(max_length=50, blank=True, null=True)
    extremidades = models.SmallIntegerField(blank=True, null=True)
    extremidades_desc = models.CharField(max_length=50, blank=True, null=True)
    piel = models.SmallIntegerField(blank=True, null=True)
    piel_desc = models.CharField(max_length=50, blank=True, null=True)
    neurologico = models.SmallIntegerField(blank=True, null=True)
    neurologico_desc = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Examen_fisico'
        unique_together = (('dia', 'no_inclusion'),)


class ExamenLabClinico(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    dia = models.IntegerField()
    fecha_hematologicos = models.DateField(blank=True, null=True)
    hemoglobina_valor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    hemoglobina = models.SmallIntegerField(blank=True, null=True)
    ctl_valor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    ctl = models.SmallIntegerField(blank=True, null=True)
    neutrofilos_valor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    neutrofilos = models.SmallIntegerField(blank=True, null=True)
    linfocitos_valor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    linfocitos = models.SmallIntegerField(blank=True, null=True)
    monocitos_valor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    monocitos = models.SmallIntegerField(blank=True, null=True)
    basofilos_valor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    eosinofilos = models.SmallIntegerField(blank=True, null=True)
    eosinofilos_valor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    basofilos = models.SmallIntegerField(blank=True, null=True)
    c_plaquetas_valor = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    c_plaquetas = models.SmallIntegerField(blank=True, null=True)
    eritro_valor = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    eritro = models.SmallIntegerField(blank=True, null=True)
    fecha_quimica_sanguinea = models.DateField(blank=True, null=True)
    creatinina_valor = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    creatinina = models.SmallIntegerField(blank=True, null=True)
    tgo_valor = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    tgo = models.SmallIntegerField(blank=True, null=True)
    tgp_valor = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    tgp = models.SmallIntegerField(blank=True, null=True)
    glicemia_valor = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    glicemia = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Examen_lab_clinico'
        unique_together = (('no_inclusion', 'dia'),)


class Fallecimiento(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    causa_clinica = models.CharField(max_length=50, blank=True, null=True)
    realizo_necrosia = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Fallecimiento'


class Frecuencia(models.Model):
    tipo = models.CharField(primary_key=True, max_length=20)

    class Meta:
        db_table = 'Frecuencia'


class Germen(models.Model):
    #dia = models.SmallIntegerField()
    nombre = models.CharField(max_length=30, primary_key=True)

    class Meta:
        db_table = 'Germen'
        #unique_together = (('dia', 'nombre'),)


class InterrupcionTratamiento(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    dosis_recibidas = models.SmallIntegerField(blank=True, null=True)
    abandono_voluntario = models.SmallIntegerField(blank=True, null=True)
    criterios_exclusion = models.SmallIntegerField(blank=True, null=True)
    eventos_adversos = models.SmallIntegerField(blank=True, null=True)
    aparicion_agravamiento = models.SmallIntegerField(blank=True, null=True)
    fallecimiento = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Interrupcion_tratamiento'


class ManifestacionesClinicas(models.Model):
    dia = models.IntegerField()
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    induracion = models.SmallIntegerField(blank=True, null=True)
    edema_local = models.SmallIntegerField(blank=True, null=True)
    eritema_diametro = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    sensibilidad = models.SmallIntegerField(blank=True, null=True)
    dolor_local = models.SmallIntegerField(blank=True, null=True)
    calor_local = models.SmallIntegerField(blank=True, null=True)
    secrecion_purulenta = models.SmallIntegerField(blank=True, null=True)
    secrecion_no_purulenta = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Manifestaciones_clinicas'
        unique_together = (('dia', 'no_inclusion'),)


class ManifestacionesClinicasOtras(models.Model):
    #
    nombre = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'Manifestaciones_clinicas_otras'
        # unique_together = (('dia', 'nombre'),)


class Medicamento(models.Model):
    nombre = models.CharField(primary_key=True, max_length=50)

    class Meta:
        db_table = 'Medicamento'


class Necrosia(models.Model):
    no_inclusion = models.ForeignKey('Paciente', db_column='no_inclusion')
    hallazgo = models.CharField(max_length=50, blank=True, null=True)
    #hallazgo2 = models.CharField(max_length=50, blank=True, null=True)
    #hallazgo3 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Necrosia'
        unique_together = (('no_inclusion', 'hallazgo'),)


class Paciente(models.Model):
    no_inclusion = models.SmallIntegerField(primary_key=True)
    fecha_inclusion = models.DateField(blank=True, null=True)
    edad = models.SmallIntegerField(blank=True, null=True)
    sexo = models.SmallIntegerField(blank=True, null=True)
    raza = models.SmallIntegerField(blank=True, null=True)
    iniciales = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        db_table = 'Paciente'


class RelacionPacCausasInterrupOtras(models.Model):
    no_inclusion = models.ForeignKey(Paciente, db_column='no_inclusion')
    nombre = models.ForeignKey(CausasInterrupcionOtras, db_column='nombre')


    class Meta:
        db_table = 'Relacion_pac_causas_interrup_otras'
        unique_together = (('no_inclusion', 'nombre'),)


class RelacionPacManiClinOtras(models.Model):
    no_inclusion = models.ForeignKey(Paciente, db_column='no_inclusion')
    dia = models.SmallIntegerField()
    nombre = models.ForeignKey(ManifestacionesClinicasOtras, db_column='nombre')

    class Meta:
        db_table = 'Relacion_pac_mani_clin_otras'
        unique_together = (('no_inclusion', 'dia', 'nombre'),)


class RelacionPacienteGermen(models.Model):
    no_inclusion = models.ForeignKey(Paciente, db_column='no_inclusion')
    dia = models.SmallIntegerField()
    nombre = models.ForeignKey(Germen,db_column='nombre')

    class Meta:
        db_table = 'Relacion_paciente_germen'
        unique_together = (('no_inclusion', 'dia', 'nombre'),)


class TratamientoConcomitante(models.Model):
    no_inclusion = models.ForeignKey(Paciente, db_column='no_inclusion')
    medida = models.ForeignKey('Unidad', db_column='medida')
    tipo = models.ForeignKey(Frecuencia, db_column='tipo')
    nombre = models.ForeignKey(Medicamento, db_column='nombre')
    tratar_eventos_adversos = models.SmallIntegerField(blank=True, null=True)
    dosis = models.SmallIntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    duracion_24_horas = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'Tratamiento_concomitante'
        unique_together = (('no_inclusion', 'nombre'),)


class Unidad(models.Model):
    medida = models.CharField(primary_key=True, max_length=20)

    class Meta:
        db_table = 'Unidad'
