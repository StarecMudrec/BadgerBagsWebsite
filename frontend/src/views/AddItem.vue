<template>
  <div class="add-item-page">
    <h1>Add New Item</h1>
    <p>This page will contain the form for adding a new item.</p>
    <router-link to="/" class="back-button">Back to Home</router-link>
  </div>
</template>

<script>
export default {
  name: 'AddItem',
}
</script>

<style scoped>
.add-item-page {
  padding: 2rem;
  text-align: center;
  min-height: 100vh;
  background: linear-gradient(to bottom, #f3efeb 0%, #e7e2dc 100%);
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
}

.back-button {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #423125;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #2a1f18;
}
</style>