<template>
  <div class="chat-container w-full max-w-lg mx-auto my-8">
    <h1 class="text-center text-2xl font-bold text-primary mb-4">
      Parkinson's Support Chatbot
    </h1>
    
    <div class="chat-box p-4 bg-base-100 rounded-lg shadow-lg">
      <div v-for="(chat, index) in chatLog" :key="index" class="mb-4">
        <div v-if="chat.sender === 'user'" class="chat chat-end">
          <div class="chat-bubble chat-bubble-primary">{{ chat.message }}</div>
        </div>
        <div v-if="chat.sender === 'bot'" class="chat chat-start">
          <div class="chat-bubble chat-bubble-secondary">{{ chat.message }}</div>
        </div>
      </div>
      <div class="input-container flex items-center mt-4">
        <input
          v-model="userMessage"
          class="input input-bordered w-full"
          placeholder="Type your message..."
          @keyup.enter="sendMessage"
        />
        <button
          @click="sendMessage"
          class="btn btn-primary ml-2"
        >
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userMessage: "",
      chatLog: []
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === "") return;

      // Add the user's message to the chat log
      this.chatLog.push({ sender: "user", message: this.userMessage });

      const userInput = this.userMessage;
      this.userMessage = ""; // Clear the input field

      try {
        // Send the message to the backend
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
    }
  }
};
</script>

<style scoped>
.chat-container {
  max-width: 600px;
}

.chat-box {
  background-color: #f8f9fa;
}

.chat-bubble-primary {
  background-color: #4f46e5;
  color: white;
}

.chat-bubble-secondary {
  background-color: #93c5fd;
  color: white;
}
</style>
