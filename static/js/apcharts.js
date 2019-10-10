
Highcharts.setOptions({
global: {
        useUTC: false
    }
});
function activeLastPointToolip(chart) {
	var points1 = chart.series[0].points,
		points2 = chart.series[1].points;
	if (points1.length > 2) {
		chart.tooltip.refresh([points1[points1.length - 1], points2[points2.length - 1]]);
	}
}
function addChartValue(chart,y1,y2) {
    var series1 = chart.series[0];
    var series2 = chart.series[1];
    var x = (new Date()).getTime();
    shift = series1.data.length > 20;
    series1.addPoint([x, y1], false, shift, true);
    series2.addPoint([x, y2], true, shift, true);
    activeLastPointToolip(chart);
}

Highcharts.setOptions({
    lang: {
        noData: '暂无数据'
    }
});
var netchart = Highcharts.chart('net-chart', {
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
		data: []},
        {
		type: 'areaspline',
		name: 'down',
        color: '#00ACEC',
        fillOpacity: 0.5,
		data: []}
	]
});

var iochart = Highcharts.chart('io-chart', {
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
        valueDecimals: 0,
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
		data: []},
        {
		type: 'areaspline',
		name: 'write',
        color: '#00ACEC',
        fillOpacity: 0.5,
		data: []}
	]
});