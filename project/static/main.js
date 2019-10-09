function requestGet(url, onSuccess) {
    onSuccess = onSuccess || function(){};
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            console.log("xhttp.responseText = " + xhttp.responseText);
            onSuccess(xhttp.responseText);
        }
    };
    xhttp.onerror = function() {
        throw new TypeError('Network request failed!');
    };
    xhttp.ontimeout = function() {
        throw new TypeError('Network request timeout!');
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

function requestPost(url, data, onSuccess) {
    onSuccess = onSuccess || function(){};
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 202) {
            console.log("xhttp.responseText = " + xhttp.responseText);
            var data = JSON.parse(xhttp.responseText).data;
            onSuccess(data.task_id);
        }
    };
    xhttp.onerror = function() {
        throw new TypeError('Network Request failed!');
    };
    xhttp.ontimeout = function() {
        throw new TypeError('Network Request timeout!');
    };
    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(data));
}

function getStatus(taskID) {
    var url='http://localhost:5000/tasks/'+taskID;
    requestGet(url, function(res) {
        var data = JSON.parse(res).data;
        var tsk_brd = document.getElementById('tasks');
        //var newRow  = tsk_brd.insertRow(tsk_brd.rows.length); // append
        var newRow  = tsk_brd.insertRow(0);  // prepend
        var new_id      = newRow.insertCell(0);
        var new_status  = newRow.insertCell(1);
        var new_result  = newRow.insertCell(2);
        var dat_id      = document.createTextNode(data.task_id);
        var dat_status  = document.createTextNode(data.task_status);
        var dat_result  = document.createTextNode(data.task_result);
        new_id.appendChild(dat_id);
        new_status.appendChild(dat_status);
        new_result.appendChild(dat_result);
        const taskStatus = data.task_status;
        if (taskStatus === 'finished' || taskStatus === 'failed')
            return false;
        setTimeout(function() {
            getStatus(data.task_id);
        }, 1000);
    });
}

function bind() {
    var btn_save = document.getElementById('btn_save');
    btn_save.onclick = function() {
        var url='http://localhost:5000/tasks';
        var data={type: 'SAVE'};
        requestPost(url, data, getStatus);
    };

    var btn_load = document.getElementById('btn_load');
    btn_load.onclick = function() {
        var url='http://localhost:5000/tasks';
        var data={type: 'LOAD'};
        requestPost(url, data, getStatus);
    };
};

