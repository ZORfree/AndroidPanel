
$(document).ready(function() {
    namespace = '/proPage';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    var cpuCount = 0;
    var cpuSum = 0.0;
    var cpuMax = 0.0;
    var pssCount = 0;
    var pssSum = 0.0;
    var pssMax = 0.0;
    socket.on('server_response', function(msg) {
        console.log('Received #' + ': ' + JSON.stringify(msg));
        if (7 == msg.category){
            cpuCount += 1;
            cpuSum += msg.data;
            if (msg.data > cpuMax){
                cpuMax = msg.data
            }
            console.log("CPU Average : "+(cpuSum/cpuCount).toFixed(1) + "MAX: "+cpuMax);
            document.getElementById('CPUAverage').text = (cpuSum/cpuCount).toFixed(1) + ' %';
            document.getElementById('CPUMax').text = cpuMax + ' %';
            addCPChartValue(cpuchart,msg.data)
        }
        if (8 == msg.category){
            pssCount += 1;
            pssSum += msg.used;
            if (msg.used > pssMax){
                pssMax = msg.used
            }
            console.log("PSS Average : "+ (pssSum/pssCount).toFixed(1) + "MAX: "+pssMax);
            document.getElementById('PSSAverage').text = (pssSum/pssCount).toFixed(1) + ' MB';
            document.getElementById('PSSMax').text = pssMax + ' MB';
            addCPChartValue(psschart,msg.used)
        }
        if (9 == msg.category){
            document.getElementById('up').text = msg.up + ' Kb';
            document.getElementById('upT').text = msg.TotalSnd;
            document.getElementById('downT').text = msg.TotalRcv;
            document.getElementById('down').text = msg.down + ' Kb';
            addChartValue(netchart,msg.up,msg.down)
        }
        if (10 == msg.category){
            document.getElementById('read').text = msg.read + ' Kb';
            document.getElementById('readT').text = msg.totalRead;
            document.getElementById('writeT').text = msg.totalWrite;
            document.getElementById('write').text = msg.write + ' Kb';
            addChartValue(iochart,msg.read,msg.write)
        }
        })
});
