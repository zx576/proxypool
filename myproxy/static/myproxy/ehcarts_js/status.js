/**
 * Created by zhouxin on 2017/4/12.
 */



var func_status = function (status_data) {
    // console.log(status_data);
    // console.log(status_data['titles']);
    option = {
    title : {
        text: status_data['title_text'],
        subtext: status_data['title_subtext'],
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        // data: ['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
        data: status_data['legend_data']
    },
    series : [
        {
            name: status_data['series_name'],
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            // data:[
            //     {value:335, name:'直接访问'},
            //     {value:310, name:'邮件营销'},
            //     {value:234, name:'联盟广告'},
            //     {value:135, name:'视频广告'},
            //     {value:1548, name:'搜索引擎'}
            // ],
            data:status_data['series_data'],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
return option
};