function platingColour(value) {
                //标准正常值 是70分
                if (value>75){
                    return '#1FAC77'
                }if (value>60){
                    return '#FF9900'
                }return '#D83125'
            }
            var reportScore = 100;
$.getJSON(window.location.href + 'reportScore', function (reportScore) {
    $(".ScoreChart").circleChart({
        color: platingColour(reportScore),
        widthRatio: 0.2, //线宽
        value: reportScore,
        startAngle: 180, //开始位置
        speed: 500,
        textWeight: 'normal', //文字粗细
        textFamily: 'fantasy', //字体
        textSize: "3em",
        text: reportScore,
        size: 120,
        animation: "linearTween" //动画类型
    });
});

Highcharts.setOptions({
global: {
        useUTC: false
    }
});

Highcharts.setOptions({
    lang: {
        noData: '暂无数据'
    }
});
$.getJSON(window.location.href + 'CPU', function (data) {
    if (data) {
        Highcharts.chart('cpu-chart', {
            exporting: {
                enabled: true
            },
            credits: {
                enabled: false // 禁用版权信息
            },
            chart: {
                zoomType: 'x'
            },
            title: {
                text: ''
            },
            subtitle: {},
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<small>{point.key}</small><table>',
                pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                    '<td style="text-align: right"><b>{point.y} %</b></td></tr>',
                footerFormat: '</table>',
                valueDecimals: 2,
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%Y-%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: false// 禁用图例信息
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false,// 禁用 数据点
                        radius: 2 //数据点 半径
                    },
                    lineWidth: 1, // 线宽
                    states: {
                        hover: {
                            lineWidth: 1 //有焦点时的线宽
                        }
                    }
                }
            },
            series: [{
                type: 'spline',
                name: 'cpu',
                color: '#F8A326',
                data: data
            }]
        });
    }
});


$.getJSON(window.location.href + 'PSS', function (data) {
    if (data) {
        Highcharts.chart('pss-chart', {
            exporting: {
                enabled: true
            },
            credits: {
                enabled: false // 禁用版权信息
            },
            chart: {
                zoomType: 'x'
            },
            title: {
                text: ''
            },
            subtitle: {},
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<small>{point.key}</small><table>',
                pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                    '<td style="text-align: right"><b>{point.y}</b></td></tr>',
                footerFormat: '</table>',
                valueDecimals: 2,
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%Y-%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: false// 禁用图例信息
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false,// 禁用 数据点
                        radius: 2 //数据点 半径
                    },
                    lineWidth: 1, // 线宽
                    states: {
                        hover: {
                            lineWidth: 1 //有焦点时的现款
                        }
                    }
                }
            },
            series: [{
                type: 'spline',
                name: 'memory',
                color: '#00ACEC',
                data: data
            }]
        });
    }
});


$.getJSON(window.location.href + 'PSS', function (data) {
    if (data) {
        Highcharts.chart('pss-chart', {
            exporting: {
                enabled: true
            },
            credits: {
                enabled: false // 禁用版权信息
            },
            chart: {
                zoomType: 'x'
            },
            title: {
                text: ''
            },
            subtitle: {},
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<small>{point.key}</small><table>',
                pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                    '<td style="text-align: right"><b>{point.y}</b></td></tr>',
                footerFormat: '</table>',
                valueDecimals: 2,
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%Y-%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: false// 禁用图例信息
            },
            plotOptions: {
                spline: {
                    marker: {
                        enabled: false,// 禁用 数据点
                        radius: 2 //数据点 半径
                    },
                    lineWidth: 1, // 线宽
                    states: {
                        hover: {
                            lineWidth: 1 //有焦点时的现款
                        }
                    }
                }
            },
            series: [{
                type: 'spline',
                name: 'memory',
                color: '#00ACEC',
                data: data
            }]
        });
    }
});

$.getJSON(window.location.href + 'NET', function (data) {
    if (data){
        Highcharts.chart('net-chart', {
            exporting: {
                enabled: true
            },
            credits:{
             enabled: false // 禁用版权信息
            },
            chart: {
                zoomType: 'x'
            },
            title: {
                text: ''
            },
            subtitle: {
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<small>{point.key}</small><table>',
                pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                '<td style="text-align: right"><b>{point.y} Kb/s</b></td></tr>',
                footerFormat: '</table>',
                valueDecimals: 1,
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%Y-%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: true// 禁用图例信息
            },
            plotOptions: {
                areaspline: {
                    marker: {
                        enabled: false,// 禁用 数据点
                        radius: 2 //数据点 半径
                    },
                    lineWidth: 1, // 线宽
                    states: {
                        hover: {
                            lineWidth: 1 //有焦点时的线宽
                        }
                    }
                }
            },
            series: [{
                type: 'areaspline',
                name: 'up',
                color: '#F8A326',
                data: data[0]},
                {
                type: 'areaspline',
                name: 'down',
                color: '#00ACEC',
                fillOpacity: 0.5,
                data: data[1]
                }
            ]
        });
    }
});

$.getJSON(window.location.href + 'IO', function (data) {
    if (data){
        Highcharts.chart('io-chart', {
            exporting: {
                enabled: true
            },
            credits:{
             enabled: false // 禁用版权信息
            },
            chart: {
                zoomType: 'x'
            },
            title: {
                text: ''
            },
            subtitle: {
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            tooltip: {
                shared: true,
                useHTML: true,
                headerFormat: '<small>{point.key}</small><table>',
                pointFormat: '<tr><td style="color: {series.color}">{series.name}: </td>' +
                '<td style="text-align: right"><b>{point.y} Kb/s</b></td></tr>',
                footerFormat: '</table>',
                valueDecimals: 1,
                dateTimeLabelFormats: {
                    millisecond: '%H:%M:%S.%L',
                    second: '%H:%M:%S',
                    minute: '%H:%M',
                    hour: '%H:%M',
                    day: '%Y-%m-%d',
                    week: '%m-%d',
                    month: '%Y-%m',
                    year: '%Y'
                }
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            legend: {
                enabled: true// 禁用图例信息
            },
            plotOptions: {
                areaspline: {
                    marker: {
                        enabled: false,// 禁用 数据点
                        radius: 2 //数据点 半径
                    },
                    lineWidth: 1, // 线宽
                    states: {
                        hover: {
                            lineWidth: 1 //有焦点时的现款
                        }
                    }
                }
            },
            series: [{
                type: 'areaspline',
                name: 'read',
                color: '#F8A326',
                data: data[0]},
                {
                type: 'areaspline',
                name: 'write',
                color: '#00ACEC',
                fillOpacity: 0.5,
                data: data[1]
                        }
                    ]
                });
    }
});

