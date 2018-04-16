<template>
  <div id="Bigone">
    <transition name="fade">
      <div id="hover" v-if="!isStart && !init" @click="$emit('start')">
        <p>点击以开始..</p>
      </div>
    </transition>
    <div class="container">
      <div id="descriptions">
        <div>
          <div id="status" :class="dataSet.seg">{{status}}</div>
          <div id="suggestion">{{suggestion}}</div>
        </div>
        <i class="iconfont icon-laughing-" :class="em_seg"></i>
      </div>
      <div id="line-chart"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Bigone",
  data() {
    return {
      seg: "good",
      dataSet: {
        rank:'good'
      },
      nowCount: 0
    };
  },
  props: ["isStart", "init"],
  computed: {
    status: function() {
      if (this.dataSet.rank === "good") return "非常好！";
      else if (this.dataSet.rank === "soso") return "还行吧..";
      else if (this.dataSet.rank === "alert") return "我觉得不行";
      else return "emmmm..";
    },
    em_seg: function() {
      return "em-" + this.dataSet.rank;
    },
    suggestion: function() {
      if (this.dataSet.rank === "good") return "继续保持";
      else if (this.dataSet.rank === "soso") return "皮一下，活跃气氛";
      else if (this.dataSet.rank === "alert") return "这就很尴尬了";
      else return "oops";
    }
  },
  mounted: function() {
    let that = this;
    let LineChart = echarts.init(
      document.getElementById("line-chart"),
      "walden"
    );
    let loption = {
      xAxis: {
        type: "category",
        boundaryGap: false,
        axisLabel: { show: false }
      },
      yAxis: {
        type: "value",
        boundaryGap: false
      },
      series: [
        {
          data: [60, 25, 23, 96, 56],
          type: "line",
          areaStyle: {}
        }
      ]
    };
    LineChart.setOption(loption);
    setInterval(function() {
      console.log(that.isStart);
      if (that.isStart) {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = () => {
          if (xhr.readyState == 4 && xhr.status == 200) {
            let response = xhr.responseText;
            console.log(response);
            let datas = JSON.parse(response);
            that.dataSet = datas;
            if (datas.framecount) {
              if (loption.series[0].data.length > 5)
                loption.series[0].data.shift();
              loption.series[0].data.push(datas.score + 100);
              LineChart.setOption(loption);
              that.nowCount = datas.framecount;
            }
          }
        };
        xhr.open("GET", "http://localhost:3000/", true);
        xhr.send(null);
      }
    }, 5000);
  }
};
</script>

<style scoped>
#hover {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  z-index: 10000;
  background-color: rgb(63, 177, 227);
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease;
}
#hover:hover {
  background-color: rgb(22, 168, 231);
}
#hover > p {
  color: white;
  font-size: 8rem;
}

#Bigone {
  height: calc(100% - 3rem);
  background-color: whitesmoke;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  position: relative;
  display: flex;
}

#descriptions {
  display: inline-flex;
  align-items: center;
}
#descriptions > i {
  transition: all 0.2s ease;
  font-size: 10rem;
}
#status {
  font-size: 8rem;
  transition: all 0.2s ease;
}
#suggestion {
  display: inline-block;
  font-size: 4rem;
  color: #333;
}

#bar-chart {
  height: 3rem;
  width: 30rem;
}

#line-chart {
  display: inline-block;
  margin-left: 2rem;
  height: 20rem;
  width: 30rem;
}
.good {
  color: rgb(63, 177, 227) !important;
}
.soso {
  color: rgb(238, 221, 120) !important;
}
.alert {
  color: rgb(217, 88, 80) !important;
}

.em-good {
  color: rgb(238, 221, 120) !important;
}
.em-soso {
  color: rgb(98, 108, 145) !important;
}
.em-alert {
  color: rgb(217, 88, 80) !important;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
</style>
