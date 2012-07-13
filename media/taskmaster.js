function addTask() {
    // Form handler: wird immer aufgerufen, wenn eine neue Position der Bestellung zugefügt wird
    // oder eine Position manuel geaendert wird.
    var person = $('#taskeingabe #peep').val();
    var task = $('#taskeingabe #task').val();
    addTask_helper(person, task, '');
    $('#taskeingabe #task').val("");
    $('#taskeingabe #peep').val("").focus();
};

function addTask_helper(person, task, taskid) {
    // neu zufügen - eine Zeile konstruieren
    var textToInsert = '';
    var tdiv = $('<li class="progress"/>');
    textToInsert  += '<span class="person">' + person + '</span><br/>';
    textToInsert  += '<a class="task" href="/ops/' + taskid + '">' + task + '</a> ';
    tdiv.append(textToInsert);
    $('#tasklist').prepend(tdiv);
    // initialize jQuery Data Dictionary
    tdiv.data('person', person);
    tdiv.data('task', task);
    if (taskid == '' || taskid == undefined) {
        // save to database
        $.get("/api/add_task", {'person': person, 'task': task},
            function(taskid) {
                // Dieser Code wird mit den Rückgabedaten vom Server aufgerufen (AJAX)
                tdiv.find(".loeschen").text("");
                tdiv.data('taskid', taskid).attr("id", taskid);
                addTaskDeleteButton(tdiv);
            });
    } else {
        tdiv.data('taskid', taskid).attr("id", taskid);
        addTaskDeleteButton(tdiv);
    };
};

function addTaskDeleteButton(tdiv) {
    // adds a delete button to a task
    tdiv.removeClass("progress");
    var dspan = $('<div class="loeschen"><abbr class="platzhalter">entfernen</abbr></div>');
    dspan.click(function(eventObject) { deleteTask(tdiv); });
    tdiv.prepend(dspan);
};

function deleteTask(tdiv) {
    var taskid = tdiv.data('taskid');
    tdiv.remove();
    $.get("/api/delete_task", {'taskid': taskid},
          function(data) {
              console.log("deleted " + taskid)
        });
};