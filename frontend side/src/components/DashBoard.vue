<template>
  <div id="Dashboard">
    <div class="container">
      <div id="BarChart"></div>
      <div id="Conclude">
        <p>{{conclude}}</p>
      </div>
      <div id="LineChart">sss</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      conclude: "下次继续努力"
    };
  },
  mounted: function() {
    let xhr = new XMLHttpRequest();
    let bar = [];
    let data = [];
    let frames = [];
    xhr.onreadystatechange = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        let response = xhr.responseText;
        console.log(response);
        let result = JSON.parse(response);

        let bar = [];
        let add = 0;
        for (let i = 0; i < result.history.length; i++) {
          frames.push(i);
          data.push(result.score[i]);
          add += result.score[i];
          if (result.rank[i] == "good") {
            bar[0]++;
          } else if (result.rank[i] == "soso") {
            bar[1]++;
          } else {
            bar[2]++;
          }
        }

        if (add / data.length > 3) {
          that.conclude = "我觉得还行";
        }
        else if (add / data.length > 2) {
          that.conclude = "我觉得还行";
        }
        else {
          that.conclude = "我觉得还行";
        }
      }
    };
    xhr.open("GET", "http://127.0.0.1:5000/history", true);
    xhr.send(null);

    let BarChart = new echarts.init(
      document.getElementById("BarChart"),
      "walden"
    );
    let Boption = {
      title: {
        text: "时段占比",
        x: "center"
      },
      tooltip: {
        trigger: "item",
        formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      legend: {
        x: "center",
        y: "bottom",
        data: ["good", "just-soso", "not so good"]
      },
      toolbox: {
        show: true,
        feature: {
          mark: { show: true },
          dataView: { show: true, readOnly: false },
          magicType: {
            show: true,
            type: ["pie", "funnel"]
          },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      calculable: true,
      series: [
        {
          name: "面积模式",
          type: "pie",
          radius: [30, 110],
          roseType: "area",
          data: [
            { value: 10, name: "good" },
            { value: 5, name: "just-soso" },
            { value: 15, name: "not so good" }
          ]
        }
      ]
    };
    BarChart.setOption(Boption);

    let LineChart = echarts.init(
      document.getElementById("LineChart"),
      "walden"
    );

    for (let i = 1; i < 2000; i++) {
      frames.push(i);
      data.push(Math.random());
    }
    let Loption = {
      tooltip: {
        trigger: "axis",
        position: function(pt) {
          return [pt[0], "10%"];
        }
      },
      title: {
        left: "center",
        text: "总体数据"
      },
      toolbox: {
        feature: {
          dataZoom: {
            yAxisIndex: "none"
          },
          restore: {},
          saveAsImage: {}
        }
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: frames
      },
      yAxis: {
        type: "value",
        boundaryGap: [0, "100%"]
      },
      dataZoom: [
        {
          type: "inside",
          start: 0,
          end: 10
        },
        {
          start: 0,
          end: 10,
          handleIcon:
            "M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z",
          handleSize: "40%",
          handleStyle: {
            color: "#fff",
            shadowBlur: 3,
            shadowColor: "rgba(0, 0, 0, 0.6)",
            shadowOffsetX: 2,
            shadowOffsetY: 2
          }
        }
      ],
      series: [
        {
          name: "总体数据随时间变化",
          type: "line",
          smooth: true,
          symbol: "none",
          sampling: "average",
          itemStyle: {
            normal: {
              color: "rgb(255, 70, 131)"
            }
          },
          areaStyle: {
            normal: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: "rgb(255, 158, 68)"
                },
                {
                  offset: 1,
                  color: "rgb(255, 70, 131)"
                }
              ])
            }
          },
          data: data
        }
      ]
    };
    LineChart.setOption(Loption);
  }
};
</script>

<style scoped>
#Dashboard {
  height: calc(100% - 3rem);
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  display: grid;
  grid-template-columns: repeat(3, 25rem);
  grid-template-rows: 23rem 12rem;
}
#BarChart {
  grid-row: 1;
  grid-column: 1/ 2;
}
#Conclude {
  grid-row: 1;
  grid-column: 2/ 4;
  display: flex;
  justify-content: center;
  align-items: center;
}
#Conclude > p {
  color: #333;
  font-size: 5rem;
  font-weight: 1.3;
}
#LineChart {
  grid-row: 2;
  grid-column: 1/ 4;
}
</style>
