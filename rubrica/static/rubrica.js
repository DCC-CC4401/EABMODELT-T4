function json_data() {
    var rubric = {};
    rubric.name = document.getElementById("rubric-title").value;
    rubric.suggested_presentation_time = Date.now();
    rubric.completed = isValidRubric();

    var json_table = [];
    var table = document.getElementById("rubric-table");

    for(var i=1, row; row = table.rows[i]; i++) {
        var row_to_append = {};
        for(var j=0, col; col = row.cells[j]; j++) {
            if (j == 0) {
                row_to_append.aspecto = col.children[0].value;
            } else {
                row_to_append[table.rows[0].cells[j].children[0].value] = col.children[0].value;
            }
        }
        if (!jQuery.isEmptyObject(row_to_append)) {
            json_table.push(row_to_append);
        }
    }
    rubric.n_compliance_lvl = table.rows[0].cells.length;
    rubric.n_evaluated_aspect = table.rows.length - 1;
    rubric.min_presentation_time = Math.round(document.getElementById("presentation_min").value*60);
    rubric.max_presentation_time = Math.round(document.getElementById("presentation_min").value*60);
    rubric.rubric = json_table;
    return JSON.stringify(rubric);
}


function lastInRow(row) {
    for (var i=row.cells.length - 1; i > 0; i--) {
        if (row.cells[i].children[0].value != "") {
            return i;
        }
    }
    return -1; // empty row
}

function isValidSum() {
    var table = document.getElementById("rubric-table");
    var max_sum = 0;
    for(var i=1, row; row = table.rows[i]; i++) {
        if (lastInRow(row) == -1) {
            continue;
        }
        max_sum += parseFloat(table.rows[0].cells[lastInRow(row)].children[0].value)
    }
    console.log(max_sum);
    return max_sum == 6;
}

function isValidScores() {
    var table = document.getElementById("rubric-table");
    var current_col = table.rows[0].cells[0];
    for(var j=1, col; col = table.rows[0].cells[j]; j++) {
        if (isNaN(col.children[0].value)) {
            return false;
        }
        if (parseFloat(current_col.children[0].value) > parseFloat(col.children[0].value)) {
            return false
        }
        current_col = col;
    }
    return true;
}

function isValidTexts() {
    // recorrer tabla y chequea que no haya intermedios vacios
    var table = document.getElementById("rubric-table");

    for(var i=1, row; row = table.rows[i]; i++) {
        for(var j=0; j < lastInRow(row); j++) {
            if (row.cells[j].children[0].value == "") {
                return false;
            }
        }
    }
    return true;
}

function isValidRubric() {
    return isValidSum() && isValidScores() && isValidTexts();
}

function addRow() {
    var table = document.getElementById("rubric-table");
    var row = table.insertRow(-1);
    for(var i=0; i<table.rows[0].cells.length; i++) {
        var newcell = row.insertCell(i);
        newcell.innerHTML = "<textarea></textarea>"
    }
}

function addColumn() {
    var table = document.getElementById("rubric-table");
    for (var i = 0; i < table.rows.length; i++) {
        var newcell = table.rows[i].insertCell(-1);
        newcell.innerHTML = "<textarea></textarea>"

    }
}

function deleteRow() {
    var table = document.getElementById("rubric-table");
    if (table.rows.length > 1) {
        table.deleteRow(-1);
    }
}

function deleteColumn() {
    var table = document.getElementById("rubric-table");
    if (table.rows[0].cells.length > 1) {
        for (var i = 0; i < table.rows.length; i++) {
            table.rows[i].deleteCell(-1);
        }
    }
}

function editTitle() {
    $("#rubric-title").prop("readonly", false)
        .focus()
}

function lostFocus() {
    $("#rubric-title").prop('readonly', true);
}

$(function () {
    $(window).keydown(function(event){
    if(event.keyCode == 13) {
        event.preventDefault();
        return false;
    }});

    $("#dialog-confirm").dialog({
        autoOpen: false,
        resizable: false,
        height: 300,
        modal: true,
        buttons: {
            "Seguir editando": function() {
                $(this).dialog("close");
                location.replace("/rubrica/" + $(this).data('rubric_id') + "/modificar/");
                // location.replace("../");
            },
            "Volver al menu": function() {
                $(this).dialog("close");
                location.replace("/rubrica/");
            }
        }
    });

    $('#rubric-form').submit(function (event) {
        event.preventDefault();

        $.ajax({
            headers: {"X-CSRFToken": token},
            type: "POST",
            url: window.location.href,
            data: json_data(),
            dataType: 'text',
            success: function (response) {
                if (isValidRubric()) {
                    $("#dialog-confirm").html("Su rúbrica fue guardada satisfactoriamente. ¿Qué desea hacer?")
                        .data('rubric_id', response)
                        .dialog('open');
                } else {
                    $("#dialog-confirm").html("Su rúbrica no es válida, por lo que se guardó como borrador (no podrá usarla para evaluar). ¿Qué desea hacer?")
                        .data('rubric_id', response)
                        .dialog('open');
                }

            }
        });
        //return false;
    });

    $("textarea").change(function(){
        if(!isValidScores()){
            $("#status-rubrica").text("inválida (arreglar puntajes) ").removeClass("completed").addClass("invalid");
        } else if(!isValidSum()){
            $("#status-rubrica").text("inválida (arreglar suma)").removeClass("completed").addClass("invalid");
        } else if(!isValidTexts()) {
            $("#status-rubrica").text("inválida (arreglar textos)").removeClass("completed").addClass("invalid");
        } else {
            $("#status-rubrica").text("válida").removeClass("invalid").addClass("completed");
        }
    });


});