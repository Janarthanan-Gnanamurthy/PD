<template>
  <div class="w-full h-64 mt-4">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale)

export default {
  name: 'TremorChart',
  components: { Line },
  props: {
    tremorData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Tremor',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  watch: {
    tremorData: {
      handler(newData) {
        this.chartData.labels = newData.map(d => d.time)
        this.chartData.datasets[0].data = newData.map(d => d.value)
      },
      deep: true
    }
  }
}
</script>