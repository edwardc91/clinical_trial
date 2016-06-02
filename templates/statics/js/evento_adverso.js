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
// Fin de configuraciones


    $(document).on('ready',function(){
        console.log( "document ready" );
        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            var name = $(this).data('name');
            $('#modal_evento_nombre').val(name);
            $('#modal_name').text(name);
        });
        $(nombre_boton_eliminar_trata).on('click',function(e){
            e.preventDefault();
            var name = $(this).data('name');
            $('#modal_trata_nombre').val(name);
            $('#modal_name_trata').text(name);
        });

        var options_evento = {
                success:function(response)
                {
                    console.log( "success" );
                    if(response.status=="True"){
                        //alert("Eliminado!");
                        var nombre=response.nombre;
                        var elementos= $(nombre_tabla+' >tbody >tr').length;
                        if(elementos==1){
                                location.reload();
                        }else{
                            $('#tr_evento_'+nombre).remove();
                            $(nombre_ventana_modal).modal('hide');
                        }
                        
                    }else{
                        alert("Hubo un error al eliminar!");
                        $(nombre_ventana_modal).modal('hide');
                    }
                }
            };

        var options_trata = {
                success:function(response)
                {
                    console.log( "success" );
                    if(response.status=="True"){
                        //alert("Eliminado!");
                        var nombre=response.nombre;
                        var elementos= $(nombre_tabla_trata+' >tbody >tr').length;
                        if(elementos==1){
                                location.reload();
                        }else{
                            $('#tr_trata_'+nombre).remove();
                            $(nombre_ventana_modal_trata).modal('hide');
                        }

                    }else{
                        alert("Hubo un error al eliminar!");
                        $(nombre_ventana_modal_trata).modal('hide');
                    }
                }
            };

        $(nombre_formulario_modal).ajaxForm(options_evento);
        $(nombre_formulario_modal_trata).ajaxForm(options_trata);
    });