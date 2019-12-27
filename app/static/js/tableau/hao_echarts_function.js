/**
 * Created by hao.ren3 on 2019/12/27.
 */

function f_echarts_financial_management(div_id, date, data, data_min, data_max, data_interval) {
    var myChart = echarts.init(document.getElementById(div_id));
    // 指定图表的配置项和数据
    var option = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            title: {
                left: 'center',
                text: '成都银行每日利息统计'
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: date
            },
            yAxis: {
                type: 'value',
                min: data_min,
                max: data_max,
                interval: data_interval,
                boundaryGap: [0, '100%']
            },
            series: [
                {
                    name:'利息(元)',
                    type:'line',
                    smooth:true,
                    symbol: 'none',
                    sampling: 'average',
                    itemStyle: {
                        color: 'rgb(255, 70, 131)'
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgb(255, 158, 68)'
                        }, {
                            offset: 1,
                            color: 'rgb(255, 70, 131)'
                        }])
                    },
                    data: data
                }
            ]
        };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}