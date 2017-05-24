


var func_source = function(data){

// app.title = '环形图';

option = {

    title: {
        text: data['title_text'],
        left: 'center'


    },

    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:data['legend_data']
    },
    series: [
        {
            name:data['series_name'],
            type:'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
                normal: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    show: true,
                    textStyle: {
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:data['series_data']
        }
    ]
};

return option
};
