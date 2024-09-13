<template>
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title">Contacts</h2>
        <ul v-if="contacts.length > 0" class="list-none">
          <li v-for="contact in contacts" :key="contact.id" class="mb-2">
            <div class="flex justify-between items-center">
              <div>
                <span class="font-bold">{{ contact.name }}</span>
                <span class="text-sm text-gray-500 ml-2">({{ contact.relationship }})</span>
                <br>
                <span class="text-sm">{{ contact.phone }} | {{ contact.email }}</span>
              </div>
              <div>
                <button class="btn btn-success btn-sm mr-2">Call</button>
                <button @click="$emit('remove-contact', contact.id)" class="btn btn-error btn-sm">Remove</button>
                </div>
            </div>
          </li>
        </ul>
        <div v-else >No Contacts Found</div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ContactList',
    props: {
      contacts: {
        type: Array,
        required: true
      }
    },
    emits: ['remove-contact']
  }
  </script>