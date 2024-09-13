<template>
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Add Relative or Friend</h2>
        <form @submit.prevent="addContact" class="form-control">
          <label class="label">
            <span class="label-text">Name</span>
          </label>
          <input v-model="newContact.name" type="text" placeholder="Name" class="input input-bordered w-full" required />
          
          <label class="label">
            <span class="label-text">Phone</span>
          </label>
          <input v-model="newContact.phone" type="tel" placeholder="Phone" class="input input-bordered w-full" required />
          
          <label class="label">
            <span class="label-text">Email</span>
          </label>
          <input v-model="newContact.email" type="email" placeholder="Email" class="input input-bordered w-full" required />
          
          <label class="label">
            <span class="label-text">Relationship</span>
          </label>
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
  </template>
  
  <script>
  import { ref } from 'vue'
  
  export default {
    name: 'AddContact',
    emits: ['contact-added'],
    setup(props, { emit }) {
      const newContact = ref({ name: '', phone: '', email: '', relationship: '' })
  
      const addContact = () => {
        emit('contact-added', { ...newContact.value })
        newContact.value = { name: '', phone: '', email: '', relationship: '' }
      }
  
      return { newContact, addContact }
    }
  }
  </script>