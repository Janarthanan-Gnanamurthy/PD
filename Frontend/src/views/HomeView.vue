<template>
  <div class="p-6">
    
    <h2 class="text-xl font-semibold mb-4">Real-Time EMG Measurements</h2>
    <div class=" p-4 rounded-md shadow-lg">
      <p v-if="emgMessage" class="text-lg">{{ emgMessage }}</p>
      <p v-else class="text-lg">No EMG data received yet.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      emgMessage: ''
    };
  },
  methods: {
    setupWebSocket() {
      const socket = new WebSocket('ws://192.168.50.231:80/ws/emg');  // Updated the port to 8000
      
      // WebSocket connection successful
      socket.onopen = () => {
        console.log("WebSocket connection established");
      };

      // Handle incoming messages
      socket.onmessage = (event) => {
        console.log("WebSocket message received:", event.data);
        this.emgMessage = event.data;  // Store the message for display
      };

      // Handle errors
      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      // Handle connection closure
      socket.onclose = () => {
        console.log("WebSocket connection closed");
      };
    }
  },
  mounted() {
    this.setupWebSocket();  // Set up WebSocket connection on component mount
  }
};
</script>

<style scoped>
/* No custom styles needed since Tailwind and DaisyUI are used */
</style>
