var nombre_tabla = "#tabla_eventos"; // id
var nombre_boton_eliminar = ".delete"; // Clase
var nombre_formulario_modal = "#form_del_evento"; //id
var nombre_ventana_modal = "#eventosModal"; // id
// Fin de configuraciones


    $(document).on('ready',function(){
        console.log( "document ready" );
        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            var name = $(this).data('name');
            $('#modal_evento_nombre').val(name);
            $('#modal_name').text(name);
        });

        var options = {
                success:function(response)
                {
                    console.log( "success" );
                    if(response.status=="True"){
                        alert("Eliminado!");
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

        $(nombre_formulario_modal).ajaxForm(options);
    });