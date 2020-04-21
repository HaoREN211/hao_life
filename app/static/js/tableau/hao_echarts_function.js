/**
 * Created by hao.ren3 on 2019/12/27.
 */

function f_echarts_line(div_id, date, data, data_min, data_max, data_interval, title, description, color) {
    var myChart = echarts.init(document.getElementById(div_id));
    // 指定图表的配置项和数据
    var option = {
            tooltip: {
                trigger: 'axis',
                position: function (pt) {
                    return [pt[0], '10%'];
                }
            },
            grid:{
                x: 70,
                x2: 10,
                y2: 30
            },
            title: {
                left: 'center',
                text: title,
                textStyle:{
                    color:color
                }
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: date,
                //  改变x轴颜色
                axisLine:{
                    lineStyle:{
                        color:color
                    }
                },
                //  改变x轴字体颜色和大小
                 axisLabel: {
                    textStyle: {
                        color: color
                    }
                }
            },
            yAxis: {
                type: 'value',
                min: data_min,
                max: data_max,
                interval: data_interval,
                boundaryGap: [0, '100%'],
                axisLine:{
                    lineStyle:{
                        color:color
                    }
                },
                //  改变x轴字体颜色和大小
                 axisLabel: {
                    textStyle: {
                        color: color
                    }
                }
            },
            series: [
                {
                    name: description,
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


function f_pie_chart(div_id, legend, data, color){
    var pie_chart_salary = echarts.init(document.getElementById(div_id));
            option = {
                title: {
                    text: '工资结构',
                    left: 'center',
                    textStyle :{
                        "color": color
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                legend: {
                    type: 'scroll',
                    orient: 'vertical',
                    right: 10,
                    top: 20,
                    bottom: 20,
                    data: legend,
                    textStyle :{
                        "color": color
                    }
                },
                series: [
                    {
                        name: '公司',
                        type: 'pie',
                        radius: '55%',
                        center: ['40%', '50%'],
                        data: data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }
                ]
            };
            pie_chart_salary.setOption(option);
}