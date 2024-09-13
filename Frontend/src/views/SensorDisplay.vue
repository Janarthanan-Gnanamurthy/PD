<template>
    <div class="card shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Sensor Readings</h2>
        <div class="grid grid-cols-3 gap-4">
          <div class="stat">
            <div class="stat-title">Tremor</div>
            <div class="stat-value">{{ sensorData.tremor.toFixed(2) }}</div>
          </div>
          <div class="stat">
            <div class="stat-title">BPM</div>
            <div class="stat-value">{{ sensorData.BPM }}</div>
          </div>
          <div class="stat">
            <div class="stat-title">EMG</div>
            <div class="stat-value">{{ sensorData.EMG.toFixed(2) }}</div>
          </div>
        </div>
  
        <!-- Tremor Chart -->
        <TremorChart :tremorData="sensorData.tremor" />
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, onUnmounted } from 'vue'
  import TremorChart from './TremorChart.vue'
  
  export default {
    name: 'SensorDisplay',
    components: {
      TremorChart
    },
    setup() {
      const sensorData = ref({ tremor: 0, BPM: 0, EMG: 0 })
      let ws
  
      const connectWebSocket = () => {
        ws = new WebSocket('ws://192.168.50.231:8000/ws')
  
        ws.onopen = () => {
          console.log("WebSocket connection established")
        }
  
        ws.onmessage = (event) => {
          sensorData.value = JSON.parse(event.data)
        }
  
        ws.onerror = (error) => {
          console.error("WebSocket error:", error)
        }
  
        ws.onclose = () => {
          setTimeout(connectWebSocket, 1000)
        }
      }
  
      onMounted(() => {
        connectWebSocket()
      })
  
      onUnmounted(() => {
        if (ws) ws.close()
      })
  
      return { sensorData }
    }
  }
  </script>
  