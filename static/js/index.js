
$(document).ready(function() {
    namespace = '/showPage';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    // var socket = io();
    socket.on('server_response', function(msg) {
        // console.log('Received #' + ': ' + JSON.stringify(msg));
        if (1 == msg.category){
            changeCircValue(".CPUChart",msg.data,msg.data + '%')
        }
        if (2 == msg.category){
            changeCircValue(".RAMChart",msg.usage,msg.usage + '%')
        }
        if (3 == msg.category){
            changeCircValue(".FPSChart",msg.cent,msg.value)
        }
        if (4 == msg.category){
            changeCircValue(".DISKChart",msg.value,msg.text)
        }
        if (5 == msg.category){
            document.getElementById('up').text = msg.up + ' Kb';
            document.getElementById('upT').text = msg.TotalSnd;
            document.getElementById('downT').text = msg.TotalRcv;
            document.getElementById('down').text = msg.down + ' Kb';

            addChartValue(netchart,msg.up,msg.down)
        }
        if (6 == msg.category){
            document.getElementById('read').text = msg.read + ' Kb';
            document.getElementById('readT').text = msg.totalRead;
            document.getElementById('writeT').text = msg.totalWrite;
            document.getElementById('write').text = msg.write + ' Kb';
            console.log("IO数据："+JSON.stringify(msg));
            addChartValue(iochart,msg.read,msg.write)
        }
        })
});
