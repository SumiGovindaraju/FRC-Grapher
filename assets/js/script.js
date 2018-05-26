var ws = new WebSocket("ws://localhost:8254");
var datasets = [];
var currentTimestamp = 0;
var chart;
var replay = false;
var paused = false;

var colors = [
    'rgb(255, 99, 132)',
    'rgb(201, 203, 207)',
    'rgb(255, 159, 64)',
    'rgb(153, 102, 255)',
    'rgb(255, 205, 86)',
    'rgb(54, 162, 235)',
	'rgb(75, 192, 192)'
];

ws.onopen = function(event) {
    $("#status").val("Connected");
}

ws.onmessage = function(event) {
    if (event.data == "Replay") {
        replay = true;
    } else if (!replay) {
        var key = JSON.parse(event.data).key;
        var value = JSON.parse(event.data).value;
        if (key == "frc-grapher-timestamp") {
            currentTimestamp = value;
        } else if (datasets[key] == undefined) {
            var datasetsLen = 0;
            for (var i in datasets) {
                datasetsLen++;
            }

            datasets[key] = {
                label: key,
                fill: false,
                backgroundColor: colors[datasetsLen % colors.length],
                borderColor: colors[datasetsLen % colors.length],
                data: [{
                    x: currentTimestamp,
                    y: value
                }]
            };
        } else {
            if (datasets[key].data[datasets[key].data.length - 1].x == currentTimestamp) {
                datasets[key].data[datasets[key].data.length - 1].y = value;
            } else {
                datasets[key].data.push({
                    x: currentTimestamp,
                    y: value
                });
            }
        }
    } else {
        datasets = JSON.parse(event.data);
    }

    config.data.datasets = [];
    for (var i in datasets) {
        config.data.datasets.push(datasets[i]);

        if (chart != undefined && !paused) {
            chart.update();
        }
    }
}

ws.onclose = function(event) {
    $("#status").val("Not Connected");
}

ws.onerror = function(event) {
    $("#status").val("Error");
}

function addDataset() {
    ws.send("Add Dataset: " + $("#add-dataset-input").val());
    $("#add-dataset-input").val("")
}

function downloadScreenshot() {
    var a = document.createElement('A');
    a.href = chart.toBase64Image().replace(/^data:image\/[^;]+/, 'data:application/octet-stream');
    a.download = "FRC Grapher Screen Shot " + (new Date()).getFullYear() + "-" + ((new Date()).getMonth()+1) + "-" + (new Date()).getDate() + " at " + 
        (new Date()).getHours()%12 + "." + (new Date()).getMinutes() + "." + (new Date()).getSeconds() + ((new Date()).getHours() <= 12 ? " AM" : " PM") + ".png";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function saveConfig() {
    ws.send("Save Config");
}

function togglePausePlay() {
    if (paused) {
        paused = false;
        $(".fa-play").addClass("fa-pause");
        $(".fa-pause").removeClass("fa-play");
    } else {
        paused = true;
        $(".fa-pause").addClass("fa-play");
        $(".fa-play").removeClass("fa-pause");
    }
}

var config = {
    type: 'line',
    data: {
        datasets: []
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Robot Data: Value vs Time'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                type: 'linear',
                position: 'bottom',
                scaleLabel: {
                    display: true,
                    labelString: 'Time'
                }
            }],
            yAxes: [{
                display: true,
                type: 'linear',
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
}

$(document).ready(function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    chart = new Chart(ctx, config);
});