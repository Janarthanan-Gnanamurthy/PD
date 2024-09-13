<template>
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Alert Log</h2>
        <ul class="list-none">
          <li v-for="(alert, index) in alerts" :key="index" class="alert mb-2" :class="alertClass(alert.type)">
            <div>
              <span class="font-bold">{{ alert.timestamp }}</span>
              <span>{{ alert.message }}</span>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  
  export default {
    name: 'AlertLog',
    setup() {
      const alerts = ref([])
  
      const fetchAlerts = async () => {
        // In a real application, you would fetch alerts from your API
        // For now, we'll use dummy data
        alerts.value = [
          { timestamp: '2023-09-13 10:30', message: 'High tremor detected', type: 'warning' },
          { timestamp: '2023-09-13 11:45', message: 'Abnormal heart rate', type: 'error' },
          { timestamp: '2023-09-13 14:20', message: 'EMG readings normalized', type: 'success' },
        ]
      }
  
      const alertClass = (type) => {
        switch (type) {
          case 'warning': return 'alert-warning'
          case 'error': return 'alert-error'
          case 'success': return 'alert-success'
          default: return 'alert-info'
        }
      }
  
      onMounted(fetchAlerts)
  
      return { alerts, alertClass }
    }
  }
  </script>