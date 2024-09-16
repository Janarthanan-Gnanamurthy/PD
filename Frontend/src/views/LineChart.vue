<template>
    <div>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    props: ['sensorData'],
    data() {
      return {
        chart: null,
        chartData: {
          labels: [], // Timestamps or sequence numbers
          datasets: [
            {
              label: 'Tremor',
              borderColor: 'rgba(255, 99, 132, 1)',
              data: [], // Will be filled with tremor data
              fill: false,
            },
          ],
        },
      };
    },
    mounted() {
      this.initChart();
    },
    methods: {
      initChart() {
        const ctx = this.$refs.chartCanvas.getContext('2d');
        this.chart = new Chart(ctx, {
          type: 'line',
          data: this.chartData,
          options: {
            responsive: true,
            scales: {
              x: { title: { display: true, text: 'Time' } },
              y: { title: { display: true, text: 'Tremor Value' } },
            },
          },
        });
      },
      updateChart() {
        if (this.sensorData) {
          const currentTime = new Date().toLocaleTimeString();
          // Limit to last 10 entries to keep chart readable
          if (this.chartData.labels.length >= 10) {
            this.chartData.labels.shift();
            this.chartData.datasets[0].data.shift();
          }
  
          this.chartData.labels.push(currentTime);
          this.chartData.datasets[0].data.push(this.sensorData.tremor);
  
          this.chart.update();
        }
      },
    },
    watch: {
      sensorData: 'updateChart',
    },
  };
  </script>
  
  <style scoped>
  canvas {
    width: 100% !important;
    height: 300px !important;
  }
  </style>