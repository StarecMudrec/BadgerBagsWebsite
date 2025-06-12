<template>
  <div>
 <div class="hero-section">
 <div class="hero-image">
 <img src="/public/background.jpg" alt="Hero Background">
 <div class="logo-overlay">
 <img src="/public/logo_noph.png" alt="Store Logo">
 </div>
 </div>
 <div class="hero-text">
 <h1>Сумочки, которые вдохновляют</h1>
 <p>Откройте для себя нашу эксклюзивную коллекцию сумок, где стиль встречается с практичностью.</p>
 </div>
 </div>
 <div class="items-grid">
 <div v-if="loading" class="loading">Загрузка товаров...</div>
      <div v-else-if="error" class="error-message">Error loading data: {{ error.message || error }}. Please try again later.</div>
 <div v-else-if="items.length === 0" class="loading">Товары не найдены.</div>
 <div v-for="item in items" :key="item.id" class="item-card" @click="navigateToItem(item.id)">
 <img :src="item.img" :alt="item.name" class="item-image">
 <h3>{{ item.name }}</h3>
 <p class="item-price">{{ item.price }} руб.</p>
      />
 </div>
 </div>
 </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
 computed: {
 ...mapState(['items', 'loading', 'error']),
 },
 methods: {
 ...mapActions(['fetchItems']),
 navigateToItem(itemId) {
 this.$router.push(`/item/${itemId}`);
 },
 },
 mounted() {
 this.fetchItems();
 },
};
</script>

<style scoped>
.hero-section {
 position: relative;
 width: 100%;
 height: 400px; /* Adjust height as needed */
 overflow: hidden;
}

.hero-image {
 width: 100%;
 height: 100%;
 position: relative;
}

.hero-image img {
 width: 100%;
 height: 100%;
 object-fit: cover;
 object-position: center 57%;
}

.logo-overlay {
  position: absolute;
  top: 100px;
  left: 50%;
 transform: translateX(-50%);
}

.logo-overlay img {
 max-width: 250px;
 max-height: 250px;
 object-fit: contain;
}

.hero-text {
 position: absolute;
 bottom: 20px;
 left: 50%;
 transform: translateX(-50%);
 text-align: center;
 color: white;
 text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
 z-index: 2;
}

.hero-text h1 {
 margin: 0;
 font-size: 2.5em;
}

.hero-text p {
 margin-top: 10px;
 font-size: 1.2em;
}

.items-grid {
 display: grid;
 grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
 gap: 20px;
  position: relative; /* Essential for z-index to work correctly relative to the background */
  margin-top: 30px; /* Push content down by the height of the background */
  z-index: 2; /* Ensure content is above the background */
  /* Add other styles for your seasons container here */
  padding-bottom: 50px;
}
.error-message {
 text-align: center;
 margin: 50px 0;
 color: #ff5555;
}

.item-card {
 background-color: white;
 border-radius: 8px;
 overflow: hidden;
 box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
 cursor: pointer;
 text-align: center;
}

.item-image {
 width: 100%;
 height: 200px; /* Adjust as needed */
 object-fit: cover;
}

.item-card h3 {
 margin: 10px 0;
 font-size: 1.2em;
 color: #333;
}

.item-price {
 margin-bottom: 15px;
 font-size: 1.1em;
 color: #007bff; /* Adjust color as needed */
}