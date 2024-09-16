<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200">
    <h1 class="text-4xl font-bold mb-8  text-white bg-blue-700  rounded-lg shadow-lg p-6">Parkinson's Monitor</h1>
    <div class="container mx-auto">
      <!-- Severity Alert -->
      <div v-if="currentAlert" :class="[
        'alert shadow-lg mb-8',
        { 'alert-warning': currentAlert.severity === 'warning',
          'alert-error': currentAlert.severity === 'danger',
          'alert-info': currentAlert.severity === 'info' }
      ]">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <div>
            <h3 class="font-bold">{{ currentAlert.title }}</h3>
            <div class="text-xs">{{ currentAlert.message }}</div>
          </div>
        </div>
        <div class="flex-none">
          <button @click="dismissAlert" class="btn btn-sm">Dismiss</button>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Sensor Display -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-4 text-indigo-700">Sensor Readings</h2>
            <div class="stats shadow">
              <div class="stat">
                <div class="stat-title">Tremor</div>
                <div class="stat-value text-primary">{{ sensorData.tremor.toFixed(2) }}</div>
              </div>
              <div class="stat">
                <div class="stat-title">BPM</div>
                <div class="stat-value text-secondary">{{ sensorData.BPM }}</div>
              </div>
              <div class="stat">
                <div class="stat-title">EMG</div>
                <div class="stat-value text-accent">{{ sensorData.EMG.toFixed(2) }}</div>
              </div>
            </div>
            <div class="mt-6"><canvas id="myChart"></canvas></div>
          </div>
        </div>

        <div class="space-y-8">
          <!-- Contacts -->
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-2xl mb-4 text-indigo-700">Contacts</h2>
              <ul v-if="contacts.length > 0" class="space-y-4">
                <li v-for="contact in contacts" :key="contact.id" class="bg-gray-100 p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <div>
                      <span class="font-bold text-lg">{{ contact.name }}</span>
                      <span class="text-sm text-gray-500 ml-2">({{ contact.relationship }})</span>
                      <p class="text-sm text-gray-600">{{ contact.phone }} | {{ contact.email }}</p>
                    </div>
                    <div class="space-x-2">
                      <button @click="call(contact.phone)" class="btn btn-sm btn-success">Call</button>
                      <button @click="removeContact(contact.id)" class="btn btn-sm btn-error">Remove</button>
                    </div>
                  </div>
                </li>
              </ul>
              <div v-else class="text-center text-gray-500">No Contacts Found</div>
            </div>
          </div>

          <!-- Add Contact -->
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title text-2xl mb-4 text-indigo-700">Add Relative or Friend</h2>
              <form @submit.prevent="addContact" class="space-y-4">
                <div class="form-control">
                  <label class="label"><span class="label-text">Name</span></label>
                  <input v-model="newContact.name" type="text" placeholder="Name" class="input input-bordered w-full" required />
                </div>
                
                <div class="form-control">
                  <label class="label"><span class="label-text">Phone</span></label>
                  <input v-model="newContact.phone" type="tel" placeholder="Phone" class="input input-bordered w-full" required />
                </div>
                
                <div class="form-control">
                  <label class="label"><span class="label-text">Email</span></label>
                  <input v-model="newContact.email" type="email" placeholder="Email" class="input input-bordered w-full" required />
                </div>
                
                <div class="form-control">
                  <label class="label"><span class="label-text">Relationship</span></label>
                  <select v-model="newContact.relationship" class="select select-bordered w-full" required>
                    <option disabled selected value="">Select relationship</option>
                    <option>Family</option>
                    <option>Friend</option>
                    <option>Caregiver</option>
                    <option>Doctor</option>
                    <option>Other</option>
                  </select>
                </div>
                
                <button type="submit" class="btn btn-primary w-full">Add Contact</button>
              </form>
            </div>
          </div>
        </div>
      </div>
        <!-- Chatbot button -->
        <button
        class="fixed bottom-4 right-4 bg-blue-600 text-white p-4 rounded-full shadow-lg z-50"
        @click="toggleChatbot"
      >
        💬 PACT Companion
      </button>
      
      <!-- Chatbot interface -->
      <div v-if="showChatbot" class="fixed bottom-20 right-4 w-80 bg-white shadow-lg rounded-lg z-50">
        <div class="flex justify-between items-center bg-blue-600 p-4 rounded-t-lg text-white">
          <h2 class="text-lg font-semibold">Support Chatbot</h2>
          <button @click="toggleChatbot" class="text-white">✖</button>
        </div>
        <div class="p-4 h-64 overflow-y-auto">
          <!-- Chat log -->
          <div v-for="(chat, index) in chatLog" :key="index" class="mb-4">
            <div v-if="chat.sender === 'user'" class="chat chat-end">
              <div class="chat-bubble chat-bubble-primary">{{ chat.message }}</div>
            </div>
            <div v-if="chat.sender === 'bot'" class="chat chat-start">
              <div class="chat-bubble chat-bubble-primary">{{ chat.message }}</div>
            </div>
          </div>
        </div>
        <div class="p-4">
          <input
            v-model="userMessage"
            type="text"
            class="input input-bordered w-full"
            placeholder="Type your message..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage" class="btn btn-primary w-full mt-2">Send</button>
        </div>
      </div>
    <!-- Alert Log Table -->
    <div class="mt-8 card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4 text-indigo-700">Alert Log</h2>
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th>Date</th>
                <th>Time</th>
                <th>Event</th>
                <th>Severity</th>
                <th>Action Taken</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(alert, index) in alertLog" :key="index" :class="{
                'bg-yellow-100': alert.severity === 'warning',
                'bg-red-100': alert.severity === 'danger',
                'bg-blue-100': alert.severity === 'info'
              }">
                <td>{{ alert.date }}</td>
                <td>{{ alert.time }}</td>
                <td>{{ alert.title }}</td>
                <td>
                  <span :class="{
                    'badge badge-warning': alert.severity === 'warning',
                    'badge badge-error': alert.severity === 'danger',
                    'badge badge-info': alert.severity === 'info'
                  }">{{ alert.severity }}</span>
                </td>
                <td>{{ alert.action }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  data() {
    return {
      patientId: '1', // This would be dynamic in a real app
      contacts: [],
      newContact: { name: '', phone: '', email: '', relationship: '' },
      sensorData: { tremor: 0, BPM: 0, EMG: 0 },
      ws: null,
      showChatbot: false, // Controls visibility of chatbot
      chatLog: [], // Stores chat messages
      userMessage: "", 
      currentAlert: null,
      alertQueue: [],
      alertLog: [],
    }
  },
  methods: {
    async fetchContacts() {
      try {
        const response = await fetch(`http://192.168.50.231:8000/patient/${this.patientId}/contacts`)
        if (response.ok) {
          this.contacts = await response.json()
        } else {
          throw new Error('Failed to fetch contacts')
        }
      } catch (error) {
        console.error('Error fetching contacts:', error)
      }
    },
    async addContact() {
      try {
        const response = await fetch(`http://192.168.50.231:8000/patient/${this.patientId}/contacts`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.newContact)
        })
        if (response.ok) {
          await this.fetchContacts() // Refresh the contact list
        } else {
          throw new Error('Failed to add contact')
        }
      } catch (error) {
        console.error('Error adding contact:', error)
      }
      this.newContact = { name: '', phone: '', email: '', relationship: '' }
    },
    async removeContact(contactId) {
      try {
        const response = await fetch(`http://192.168.50.231:8000/patient/${this.patientId}/contacts/${contactId}`, { method: 'DELETE' })
        if (response.ok) {
          await this.fetchContacts() // Refresh the contact list
        } else {
          throw new Error('Failed to remove contact')
        }
      } catch (error) {
        console.error('Error removing contact:', error)
      }
    },
    connectWebSocket() {
      this.ws = new WebSocket('ws://192.168.50.231:8000/ws')
      this.ws.onopen = () => console.log('WebSocket connection established')
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.sensorData = data
        this.checkSeverityLevels(data)
      }
      this.ws.onerror = (error) => console.error('WebSocket error:', error)
      this.ws.onclose = () => setTimeout(this.connectWebSocket, 1000)
    },

    showNextAlert() {
      if (this.alertQueue.length > 0) {
        this.currentAlert = this.alertQueue.shift()
        setTimeout(() => {
          this.dismissAlert()
        }, 1000) // Auto-dismiss after 5 seconds
      } else {
        this.currentAlert = null
      }
    },

    dismissAlert() {
      this.currentAlert = null
      this.$nextTick(() => {
        this.showNextAlert()
      })
    },
    async call(num){
      try {
        const response = await fetch(`http://192.168.50.231:8000/call/${num}`, { method: 'GET' })
        if (response.ok) {
          await console.log("Call Began") // Refresh the contact list
        } else {
          throw new Error('Failed to remove contact')
        }
      } catch (error) {
        console.error('Error removing contact:', error)
      }
    },
    toggleChatbot() {
      this.showChatbot = !this.showChatbot;
    },
    async sendMessage() {
      if (this.userMessage.trim() === "") return;
      
      // Add the user's message to the chat log
      this.chatLog.push({ sender: "user", message: this.userMessage });

      const userInput = this.userMessage;
      this.userMessage = ""; // Clear the input field

      try {
        // Send the message to the backend (replace with your API)
        const response = await fetch("http://192.168.50.231:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userInput })
        });
        const data = await response.json();

        // Add the bot's response to the chat log
        this.chatLog.push({ sender: "bot", message: data.response });
      } catch (error) {
        console.error("Error while communicating with the chatbot:", error);
      }
    },
    addAlert(severity, title, message) {
      const alert = {
        severity,
        title,
        message,
        date: new Date().toISOString().split('T')[0],
        time: new Date().toLocaleTimeString(),
        action: this.getActionTaken(severity, title)
      }
      this.alertQueue.push(alert)
      this.alertLog.unshift(alert) // Add to the beginning of the log
      if (this.alertLog.length > 50) {
        this.alertLog.pop() // Remove the oldest log if we have more than 50
      }
      if (!this.currentAlert) {
        this.showNextAlert()
      }
    },

    getActionTaken(severity, title) {
      switch (severity) {
        case 'danger':
          return 'Emergency services notified'
        case 'warning':
          return 'Caregiver alerted'
        case 'info':
        default:
          return 'Logged for review'
      }
    },

    checkSeverityLevels(data) {
      if (data.severity_level == 2) {
        this.addAlert('warning', 'Elevated Tremor', 'Tremor levels are higher than normal. Consider resting or medication.')
      } else if (data.severity_level == 3) {
        this.addAlert('danger', 'Emergency', 'Tremor levels are critically high. Please take immediate action.')
      } 

      // if (data.BPM > 120) {
      //   this.addAlert('danger', 'High Heart Rate', 'Heart rate is abnormally high. Please check on the patient.')
      // } else if (data.BPM > 100) {
      //   this.addAlert('warning', 'Elevated Heart Rate', 'Heart rate is higher than normal. Monitor closely.')
      // }
    },
  },
  mounted() {
  this.fetchContacts();
  this.connectWebSocket();

  const ctx = document.getElementById('myChart').getContext('2d');
  const labels = []; // Array to hold x-axis labels
  const tremorData = []; // Array to hold tremor data
  const maxDataPoints = 20; // Max number of data points on the chart

  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Tremor Data',
        data: tremorData,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Function to update the chart with sensorData.tremor
  const updateChart = () => {
    // Push the new tremor reading from sensorData
    tremorData.push(this.sensorData.tremor.toFixed(2));
    
    // Add a new label for the x-axis
    labels.push(`${labels.length + 1}`);
    
    // Limit the number of data points displayed to maxDataPoints
    // if (tremorData.length > 75) {
    //   this.$router.go()// Remove the oldest label
    // }

    // Update the chart
    myChart.update();
    this.checkSeverityLevels(this.sensorData)
  };

  // Update the chart every 250ms
  setInterval(updateChart, 250);
},
  beforeDestroy() {
    if (this.ws) this.ws.close()
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
}

.chat-bubble-primary {
  background-color: #4f46e5;
  color: white;
}

.chat-bubble-secondary {
  background-color: #93c5fd;
  color: white;
}

.fixed {
  position: fixed;
}

.bg-blue-600 {
  background-color: #2563eb;
}

.bg-white {
  background-color: white;
}

.p-4 {
  padding: 1rem;
}

.w-80 {
  width: 20rem;
}
</style>
