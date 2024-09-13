<template>
    <div class="card shadow-xl mt-4">
      <div class="card-body">
        <h2 class="card-title">Tremor Readings Over Time</h2>
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch, onMounted } from 'vue'
  import { Chart, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend } from 'chart.js'
  
  // Register necessary chart.js components
  Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip, Legend)
  
  export default {
    name: 'TremorChart',
    props: {
      tremorData: {
        type: Number,  // Ensure it's a number, not an array
        default: 0
      }
    },
    setup(props) {
      const chartInstance = ref(null)
      const chartCanvas = ref(null)
  
      const initializeChart = () => {
        chartInstance.value = new Chart(chartCanvas.value, {
          type: 'line',
          data: {
            labels: [], // Time labels for the x-axis
            datasets: [{
              label: 'Tremor Levels',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 2,
              data: [] // Tremor data for the y-axis
            }]
          },
          options: {
            responsive: true,
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: 'Time'
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'Tremor Level'
                }
              }
            }
          }
        })
      }
  
      const updateChart = (newData) => {
        const currentTime = new Date().toLocaleTimeString()
  
        chartInstance.value.data.labels.push(currentTime)
        chartInstance.value.data.datasets[0].data.push(newData)
  
        // Limit the number of points displayed
        if (chartInstance.value.data.labels.length > 10) {
          chartInstance.value.data.labels.shift()
          chartInstance.value.data.datasets[0].data.shift()
        }
  
        chartInstance.value.update()
      }
  
      // Use deep watching on `tremorData`
      watch(
        () => props.tremorData, 
        (newData) => {
          if (chartInstance.value) {
            updateChart(newData)
          }
        }, 
        { immediate: true } // React immediately to the initial value
      )
  
      onMounted(() => {
        initializeChart()
      })
  
      return { chartCanvas }
    }
  }
  </script>
  
  <style scoped>
  .card {
    background-color: #ffffff;
    border-radius: 0.5rem;
  }
  </style>
  