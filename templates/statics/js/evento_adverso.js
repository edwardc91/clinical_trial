// configuraciones para los eventos adversos
var nombre_tabla = "#tabla_eventos"; // id
var nombre_boton_eliminar = ".delete"; // Clase
var nombre_formulario_modal = "#form_del_evento"; //id
var nombre_ventana_modal = "#eventosModal"; // id

// configuraciones para los tratamientos concomitantes
var nombre_tabla_trata = "#tabla_trata"; // id
var nombre_boton_eliminar_trata = ".delete_tra"; // Clase
var nombre_formulario_modal_trata = "#form_del_trata"; //id
var nombre_ventana_modal_trata = "#trataModal"; // id

// configuraciones para los pacientes
var nombre_tabla_pac = "#tabla_pac"; // id
var nombre_boton_eliminar_pac = ".deletepac"; // Clase
var nombre_formulario_modal_pac = "#form_del_pac"; //id
var nombre_ventana_modal_pac = "#pacModal"; // id

//configuraciones manifestaciones clinicas otras inicial
var nombre_tabla_mani = "#tabla_mani"; // id
var nombre_boton_eliminar_mani = ".delete-mani"; // Clase
var nombre_formulario_modal_mani = "#form_del_mani"; //id
var nombre_ventana_modal_mani = "#maniOtrasModal"; // id

//configuraciones germen inicial
var nombre_tabla_ger = "#tabla_germenes"; // id
var nombre_boton_eliminar_ger = ".delete-germen"; // Clase
var nombre_formulario_modal_ger = "#form_del_ger"; //id
var nombre_ventana_modal_ger = "#germenesModal"; // id

//configuraciones manifestaciones clinicas otras final
var nombre_tabla_mani_fin = "#table_mani_fin"; // id
var nombre_boton_eliminar_mani_fin = ".delete-mani-fin"; // Clase
var nombre_formulario_modal_mani_fin = "#form_del_mani_fin"; //id
var nombre_ventana_modal_mani_fin = "#maniOtrasModalFin"; // id

//configuraciones germen final
var nombre_tabla_ger_fin = "#table_germenes_fin"; // id
var nombre_boton_eliminar_ger_fin = ".delete-germen-fin"; // Clase
var nombre_formulario_modal_ger_fin = "#form_del_ger_fin"; //id
var nombre_ventana_modal_ger_fin = "#germenesModalFin"; // id
// Fin de configuraciones


$(document).on('ready', function () {
    console.log("document ready");
    $(nombre_boton_eliminar).on('click', function (e) {
        e.preventDefault();
        var name = $(this).data('name');
        $('#modal_evento_nombre').val(name);
        $('#modal_name').text(name);
    });
    $(nombre_boton_eliminar_trata).on('click', function (e) {
        //console.log("Estoy aqui trata")
        e.preventDefault();
        var name = $(this).data('name');
        $('#modal_trata_nombre').val(name);
        $('#modal_name_trata').text(name);
    });
    $(nombre_boton_eliminar_pac).on('click', function (e) {
        e.preventDefault();
        //console.log("Estoy aqui pac")
        var inc = $(this).attr('id');
        console.log("no inc " + inc)
        var name = $(this).data('name');
        $('#modal_pac_inc').val(inc);
        $('#modal_name_pac').text(name);
    });
    $(nombre_boton_eliminar_mani).on('click', function (e) {
        e.preventDefault();
        //console.log("Estoy aqui pac")
        //var inc = $(this).attr('id');
        //console.log("no inc "+inc)
        var name = $(this).data('name');
        $('#modal_mani_nombre').val(name);
        $('#header_modal_init').text("manifestacion clinica")
        $('#pregunta_modal').text("la manifestacion clinica")
        $('#modal_name_mani').text(name);
    });
    $(nombre_boton_eliminar_ger).on('click', function (e) {
        e.preventDefault();
        //console.log("Estoy aqui pac")
        //var inc = $(this).attr('id');
        //console.log("no inc "+inc)
        var name = $(this).data('name');
        $('#modal_ger_nombre').val(name);
        $('#header_modal_ger').text("germen")
        $('#pregunta_modal_ger').text("el germen")
        $('#modal_name_ger').text(name);
    });
    $(nombre_boton_eliminar_mani_fin).on('click', function (e) {
        e.preventDefault();
        //console.log("Estoy aqui pac")
        //var inc = $(this).attr('id');
        //console.log("no inc "+inc)
        var name = $(this).data('name');
        $('#modal_mani_nombre_fin').val(name);
        $('#header_modal_fin').text("manifestacion clinica")
        $('#pregunta_modal_fin').text("la manifestacion clinica")
        $('#modal_name_mani_fin').text(name);
    });
    $(nombre_boton_eliminar_ger_fin).on('click', function (e) {
        e.preventDefault();
        //console.log("Estoy aqui pac")
        //var inc = $(this).attr('id');
        //console.log("no inc "+inc)
        var name = $(this).data('name');
        $('#modal_ger_nombre_fin').val(name);
        $('#header_modal_ger_fin').text("germen")
        $('#pregunta_modal_ger_fin').text("el germen")
        $('#modal_name_ger_fin').text(name);
    });

    var options_evento = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_evento_' + nombre).remove();
                    $(nombre_ventana_modal).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal).modal('hide');
            }
        }
    };

    var options_trata = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla_trata + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_trata_' + nombre).remove();
                    $(nombre_ventana_modal_trata).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_trata).modal('hide');
            }
        }
    };

    var options_pac = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var no_inc = response.no_inc;
                var elementos = $(nombre_tabla_pac + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_pac_' + no_inc).remove();
                    $(nombre_ventana_modal_pac).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_pac).modal('hide');
            }
        }
    };

    var options_mani = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla_mani + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_mani_' + nombre).remove();
                    $(nombre_ventana_modal_mani).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_mani).modal('hide');
            }
        }
    };

    var options_ger = {
        success: function (response) {
            //console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla_ger + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_germen_' + nombre).remove();
                    $(nombre_ventana_modal_ger).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_ger).modal('hide');
            }
        }
    };
    var options_mani_fin = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla_mani_fin + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_mani_fin_' + nombre).remove();
                    $(nombre_ventana_modal_mani_fin).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_mani_fin).modal('hide');
            }
        }
    };

    var options_ger_fin = {
        success: function (response) {
            //console.log("success");
            if (response.status == "True") {
                //alert("Eliminado!");
                var nombre = response.nombre;
                var elementos = $(nombre_tabla_ger_fin + ' >tbody >tr').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#tr_germen_fin_' + nombre).remove();
                    $(nombre_ventana_modal_ger_fin).modal('hide');
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal_ger_fin).modal('hide');
            }
        }
    };


    $(nombre_formulario_modal).ajaxForm(options_evento);
    $(nombre_formulario_modal_trata).ajaxForm(options_trata);
    $(nombre_formulario_modal_pac).ajaxForm(options_pac);
    $(nombre_formulario_modal_mani).ajaxForm(options_mani);
    $(nombre_formulario_modal_ger).ajaxForm(options_ger);
    $(nombre_formulario_modal_mani_fin).ajaxForm(options_mani_fin);
    $(nombre_formulario_modal_ger_fin).ajaxForm(options_ger_fin);
});