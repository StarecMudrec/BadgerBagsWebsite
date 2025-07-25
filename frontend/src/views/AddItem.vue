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

.add-item-button {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #423125;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.05);
  aspect-ratio: 3/4; /* Match your card aspect ratio */
  min-height: 0; /* Important for grid sizing */
  padding: 0;
  margin: 0;
}

.add-item-button:hover {
  background-color: rgba(66, 49, 37, 0.05);
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.add-item-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.plus-icon {
  width: 50px;
  height: 50px;
  transition: all 0.3s ease;
}

.add-item-button:hover .plus-icon {
  transform: scale(1.1);
}
</style>