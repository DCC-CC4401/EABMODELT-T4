function json_data() {
    var rubric = {};
    rubric.name = document.getElementById("rubric-title").value;
    rubric.suggested_presentation_time = Date.now();
    rubric.completed = true;

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
    rubric.rubric = json_table;
    return JSON.stringify(rubric);
}

function isValidRubric() {
    var table = document.getElementById("rubric-table");

    // validate first row as numbers and order of values
    var current_col = table.rows[0].cells[0];
    for(var j=0, col; col = table.rows[0].cells[j]; j++) {
        if (isNaN(col.children[0].value)) {
            return false;
        }
        if (parseFloat(current_col.children[0].value) > parseFloat(col.children[0].value)) {
            return false
        }
        current_col = col;
    }


    // validate sum of scores as 6
    var max_sum = 0;
    for(var i=1; i<table.rows.length; i++) {

        //max_sum += parseFloat(table.rows[0].cells[-1].value);
        max_sum += parseFloat(table.rows[0].cells[table.rows[0].cells.length - 1].children[0].value);
    }
    if (max_sum != 6) {
        return false
    }

    return true;
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

$(function () {
    $("#dialog-confirm").dialog({
        autoOpen: false,
        resizable: false,
        height: 300,
        modal: true,
        buttons: {
            "Seguir editando": function() {
                $(this).dialog("close");
            },
            "Volver al menu": function() {
                $(this).dialog("close");
                location.replace("../")
            }
        }
    });

    $('#rubric-form').submit(function (event) {
        event.preventDefault();

        $.ajax({
            headers: {"X-CSRFToken": token},
            type: "POST",
            url: "/rubrica/crear/",
            data: json_data(),
            dataType: 'text',
            success: function (response) {
                if (isValidRubric()) {
                    $("#dialog-confirm").html("Su rúbrica fue guardada satisfactoriamente. ¿Qué desea hacer?")
                        .dialog('open');
                } else {
                    $("#dialog-confirm").html("Su rúbrica no es válida, por lo que se guardó como borrador (no podrá usarla para evaluar). ¿Qué desea hacer?")
                        .dialog('open');
                }

            }
        });
        //return false;
    });
})