<template>
  <div ref="chartContainer" style="width: 100%; height: 400px;"></div>
</template>

<script>
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import { TooltipComponent, TitleComponent, GridComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers'; // 确保导入 CanvasRenderer

// 注册必要的组件
echarts.use([
  BarChart,
  TooltipComponent,
  TitleComponent,
  GridComponent,
  CanvasRenderer // 注册 CanvasRenderer
]);

export default {
  name: 'EChartComponent',
  props: {
    toDoItems: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartInstance: null,
    };
  },
  mounted() {
    this.initChart();
  },
  beforeUnmount() {
    if (this.chartInstance) {
      // 组件销毁前，释放ECharts实例资源
      this.chartInstance.dispose();
    }
  },
  watch: {
    toDoItems: {
      deep: true,
      handler() {
        this.updateChart();
      },
    },
  },
  methods: {
    initChart() {
      const chartDom = this.$refs.chartContainer;
      this.chartInstance = echarts.init(chartDom, null, { renderer: 'canvas' }); // 指定渲染器为 'canvas'
      this.updateChart();
    },
    updateChart() {
      const categories = this.toDoItems.map(item => item.label);
      const seriesData = this.toDoItems.map(item => item.done ? 1 : 0);
      this.chartInstance.setOption({
        title: {
          text: 'To-Do List Completion Status'
        },
        tooltip: {},
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: categories,
        },
        yAxis: {
          type: 'value',
        },
        series: [{
          name: 'Completion',
          type: 'bar',
          data: seriesData,
          itemStyle: {
            color: params => params.value === 0 ? '#ff4949' : '#43a2f2', // 未完成红色，已完成蓝色
          },
        }]
      });
    }
  }
};
</script>

<style scoped>
/* 可以在这里添加一些样式，比如设置容器的宽度和高度 */
</style>