
var circ = ['.CPUChart', '.RAMChart', '.FPSChart', '.DISKChart'];

for (let i of circ) {
    console.log(i);
    $(i).circleChart({
        color: "#1FAC77",
        widthRatio: 0.1,
        value: 0,
        startAngle: 180,
        speed: 500,
        text: 'load..',
        size: 120,
        animation: "linearTween"
    });
}
// #F54E2A 红 #D83125
//
// #1FAC77 绿色#20A53A
// #FF9900 黄色
function platingColour(value) {
    if (value>90){
        return '#D83125'
    }if (value>65){
        return '#FF9900'
    }return '#1FAC77'
}
function platingFPSColour(value) {
    if (value>60){
        return '#1FAC77'
    }if (value>25){
        return '#FF9900'
    }return '#D83125'
}
function changeCircValue(circ,value,text) {
    if (".FPSChart" == circ) {
        color = platingFPSColour(value);
    } else {
        color = platingColour(value);
    }
    $(circ).circleChart({
    color: color,
    value: value,
    redraw: false,
    speed: 300,
    startAngle: 180,
    text: 0 + '%',
    onDraw: function (el, circle) {
        $(".circleChart_text", el).html(text);
        }
    });
}