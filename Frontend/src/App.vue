<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Parkinson's Monitor</h1>
    <div class="flex flex-col md:flex-row gap-4">
      <div class="w-full md:w-1/2">
        <!-- Sensor Display -->
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
          </div>
        </div>
      </div>
      <div class="w-full md:w-1/2">
        <!-- Contacts -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h2 class="card-title">Contacts</h2>
            <ul v-if="contacts.length > 0" class="list-none">
              <li v-for="contact in contacts" :key="contact.id" class="mb-2">
                <div class="flex justify-between items-center">
                  <div>
                    <span class="font-bold">{{ contact.name }}</span>
                    <span class="text-sm text-gray-500 ml-2">({{ contact.relationship }})</span><br>
                    <span class="text-sm">{{ contact.phone }} | {{ contact.email }}</span>
                  </div>
                  <div>
                    <button @click="call(contact.phone)" class="btn btn-success btn-sm mr-2">Call</button>
                    <button @click="removeContact(contact.id)" class="btn btn-error btn-sm">Remove</button>
                  </div>
                </div>
              </li>
            </ul>
            <div v-else>No Contacts Found</div>
          </div>
        </div>

        <!-- Add Contact -->
        <div class="card bg-base-100 shadow-xl mt-4">
          <div class="card-body">
            <h2 class="card-title">Add Relative or Friend</h2>
            <form @submit.prevent="addContact" class="form-control">
              <label class="label"><span class="label-text">Name</span></label>
              <input v-model="newContact.name" type="text" placeholder="Name" class="input input-bordered w-full" required />
              
              <label class="label"><span class="label-text">Phone</span></label>
              <input v-model="newContact.phone" type="tel" placeholder="Phone" class="input input-bordered w-full" required />
              
              <label class="label"><span class="label-text">Email</span></label>
              <input v-model="newContact.email" type="email" placeholder="Email" class="input input-bordered w-full" required />
              
              <label class="label"><span class="label-text">Relationship</span></label>
              <select v-model="newContact.relationship" class="select select-bordered w-full" required>
                <option disabled selected value="">Select relationship</option>
                <option>Family</option>
                <option>Friend</option>
                <option>Caregiver</option>
                <option>Doctor</option>
                <option>Other</option>
              </select>
              
              <button type="submit" class="btn btn-primary mt-4">Add Contact</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert Log -->
    <div class="mt-4 card shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Alert Log</h2>
        <p>Placeholder for alert log information.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      patientId: '1', // This would be dynamic in a real app
      contacts: [],
      newContact: { name: '', phone: '', email: '', relationship: '' },
      sensorData: { tremor: 0, BPM: 0, EMG: 0 },
      ws: null
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
        // console.log('WebSocket message received:', event.data)
        this.sensorData = JSON.parse(event.data)
      }
      this.ws.onerror = (error) => console.error('WebSocket error:', error)
      this.ws.onclose = () => setTimeout(this.connectWebSocket, 1000)
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
    }
  },
  mounted() {
    this.fetchContacts()
    this.connectWebSocket()
  },
  beforeDestroy() {
    if (this.ws) this.ws.close()
  }
}
</script>


