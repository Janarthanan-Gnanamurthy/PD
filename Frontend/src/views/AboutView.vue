<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-4">Parkinson's Monitor</h1>
    <div class="flex flex-col md:flex-row gap-4">
      <SensorDisplay class="w-full md:w-1/2" />
      <div class="w-full md:w-1/2">
        <ContactList />
        <AddContact class="mt-4" />
      </div>
    </div>
    <AlertLog class="mt-4" />
  </div>
</template>

<script>
import SensorDisplay from './components/SensorDisplay.vue'
import ContactList from './components/ContactList.vue'
import AddContact from './components/AddContact.vue'
import AlertLog from './components/AlertLog.vue'

export default {
  name: 'App',
  components: {
    SensorDisplay,
    ContactList,
    AddContact,
    AlertLog
  }
}
</script>