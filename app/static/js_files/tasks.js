
$(document).ready(function(){

    $('#datetimepicker1, #datetimepicker2').datetimepicker({
        format: 'YYYY-MM-DD hh:mm:ss'
    });

    $(".select2_demo_3,.select2_demo_4").select2({
        placeholder: "Select",
        allowClear: true
    });


    $("form.add-task-form").submit(function(e){
        e.preventDefault()

        $.post("add_task/", $("form.add-task-form").serialize(), function(data){
            if(data["ret"] === true){
                alert(data["message"]);
                location.href = '/tasks/'
            }else{
                alert(data["message"]);
                location.reload()
            }
        });

        return false;
    });

    $("form.edit-task-form").submit(function(e){
        e.preventDefault()

        $.post("edit_task/", $("form.edit-task-form").serialize(), function(data){
            if(data["ret"] === true){
                alert(data["message"]);
                location.href = '/tasks/'
            }else{
                alert(data["message"]);
                //location.reload()
            }
        });

        return false;
    });

    $('#datetimepicker1').datetimepicker();
    
});

function open_my_row(id){   
    if($("#row-"+id).is(":visible")==false){
        $("tr.parent-rows").removeAttr("style");
        $("#parent-row-"+id).css({"background-color":"#1d1d1d","color":"#ffffff"});
        $("tr.hidden-rows").css('display','none');
        $("#row-"+id).show();
    }else{
        $("tr.parent-rows").removeAttr("style");
        $("tr.hidden-rows").css('display','none');
        $("#row-"+id).hide();
    }    
}


function remove_observers(id){
    $.post("/tasks/remove-observers/",{id:id, csrfmiddlewaretoken: csrfmiddlewaretoken}, function(data){
        location.reload()
    });
}

function remove_participants(id){
    $.post("/tasks/remove-participants/",{id:id, csrfmiddlewaretoken: csrfmiddlewaretoken}, function(data){
        location.reload()
    });
}

function task_logs(id){
    $.post("/tasks/logs/",{id:id, csrfmiddlewaretoken: csrfmiddlewaretoken}, function(data){
        $("div#task-logs-data").empty().append(data);
        $("div#modal-task-logs").modal('show');
    });
}

function get_edit_form(id){
    $.post("/tasks/edit_task_form/",{id:id, csrfmiddlewaretoken: csrfmiddlewaretoken}, function(data){
        $("div#form-template").empty().append(data);
        $("#modal-edit-task").modal('show');
    });
}

