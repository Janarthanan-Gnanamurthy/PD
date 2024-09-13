<template>
    <div class="card  shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Contacts</h2>
        <ul class="list-none">
          <li v-for="contact in contacts" :key="contact.email" class="mb-2">
            <div class="flex justify-between items-center">
              <span>{{ contact.name }} - {{ contact.phone }}</span>
              <button @click="removeContact(contact)" class="btn btn-error btn-xs">Remove</button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  
  export default {
    name: 'ContactList',
    setup() {
      const contacts = ref([])
  
      const fetchContacts = async () => {
        const response = await fetch('http://192.168.50.231:8000/patient/1/contacts')
        contacts.value = await response.json()
      }
  
      const removeContact = async (contact) => {
        // Implement remove contact logic here
        // This would typically involve a DELETE request to your API
        // After successful deletion, call fetchContacts() to update the list
      }
  
      onMounted(fetchContacts)
  
      return { contacts, removeContact }
    }
  }
  </script>