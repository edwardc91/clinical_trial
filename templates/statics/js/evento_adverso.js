/**
 * Created by root on 30/05/16.
 */

function delete_evento_adverso(nombre, url) {
    $.ajax({
        type: 'POST',
        url: url,
        data: {nombre: nombre},
        dataType: 'json',
        success: evento_delete_confirm,
        error: function () {
            alert('AJAX error.');
        }
    });
}

function evento_delete_confirm(response) {
    evento_nombre = JSON.parse(response);
    // This line is in the function that receives the AJAX response when
    //the request was successful. This line allows deserializing the JSON
    //response returned by Django views.
    if (evento_nombre>0) {
        $('#evento_'+ evento_nombre).remove();
        //This line will delete the <tr> tag containing the task we have just removed
    }
    else {
        alert('Error');
    }
}