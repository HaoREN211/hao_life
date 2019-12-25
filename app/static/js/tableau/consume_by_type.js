/**
 * Created by hao.ren3 on 2019/12/25.
 */

function f_consume_by_type() {
    var f_consume_by_type = echarts.init(document.getElementById('consume_by_type'));

    var f_oAjax = null;
    var f_postData = {"vote_id": "{{ vote.id }}"};
    f_postData="vote_id="+"{{ vote.id }}";

    try{
    　　f_oAjax = new XMLHttpRequest();
    }catch(e){
    　　f_oAjax = new ActiveXObject("Microsoft.XMLHTTP");
    }

    var f_url = '/data/consume_by_type';
    //post方式打开文件
    f_oAjax.open('post', f_url, true);

    //post相比get方式提交多了个这个
    f_oAjax.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    //post发送数据
    f_oAjax.send(f_postData);
    f_oAjax.onreadystatechange = function(){
        //当状态为4的时候，执行以下操作
    　　if(f_oAjax.readyState === 4){
            try{
                var f_echart_response = f_oAjax.responseText;
                // 转化为json字符串
                var f_obj = JSON.parse(f_echart_response);

                console.log(f_echart_response);
                console.log(f_obj);
                // 转化为json对象
                f_obj = eval("("+f_obj+")");
                console.log(f_obj);

                var f_option = {
                    title: {
                        text: '消费种类统计',
                        left: 0,
                        top: 0,
                        textStyle: {
                            color: '#ffffff'
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        backgroundColor : 'rgba(0,0,250,0.2)'
                    },
                    radar: {
                        indicator : f_obj.types,
                        center: ['50%', '60%'],
                        axisLine: {                         // (圆内的几条直线)坐标轴轴线相关设置
                                lineStyle: {
                                    color: '#fff',                   // 坐标轴线线的颜色。
                                    width: 1,                      	 // 坐标轴线线宽。
                                    type: 'solid'                    // 坐标轴线线的类型。
                                }
                            }
                    },
                    series : [{
                        name:'消费种类',
                        type: 'radar',
                        symbol: 'none',
                        lineStyle: {
                            width: 1
                        },
                        // 高亮时的样式
                        emphasis: {
                            areaStyle: {
                                color: 'rgba(250,0,0,1)'
                            }
                        },
                        data:[
                          {
                            value:f_obj.data,
                              areaStyle: {                // 单项区域填充样式
                                normal: {
                                    color: 'rgba(255,0,0,0.5)'       // 填充的颜色。
                                }
                            }
                          }
                        ]
                    }]
                };

                // 使用刚指定的配置项和数据显示图表。
                f_consume_by_type.setOption(f_option);
            }catch(e){
    　　　　　　alert('你访问的页面出错了');
    　　　　}
        }
    }
}

f_consume_by_type();





