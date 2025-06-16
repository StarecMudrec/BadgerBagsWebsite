<template>
  <!-- Фон (прижат к самому верху) -->
  <div class="background-wrapper">
    <div class="background-container"></div>
  </div>
  
  <!-- Линия-разделитель -->
  <hr class="separator-line" />
  
  <!-- Основной контент -->
  <div class="content">
    <div class="bag-catalog">
      <BagCard v-for="bag in bags" :key="bag.id" :bag="bag" />
    </div>
  </div>
</template>

<script>
import BagCard from '@/components/BagCard.vue';

export default {
  components: {
    BagCard
  },
  data() {
    return {
      bags: []
    };
  },
  async created() {
    const response = await fetch('/api/bags');
    this.bags = await response.json();
  }
};
</script>

<style scoped>
/* Жёсткий сброс всех отступов */
body, html, #app {
  margin: 0 !important;
  padding: 0 !important;
}

.page-container {
  min-height: 100vh;
}

/* Обёртка для фона */
.background-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -1;
}

/* Сам фон */
.background-container { 
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
}

/* Линия разделения */
.separator-line {
  position: absolute;
  top: 100vh;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: white;
  margin: 0;
  border: none;
}

/* Основной контент */
.content {
  position: absolute;
  margin-top: 100vh;
  width: 100%;
  min-height: calc(100vh - 4px);
  left: 0;
  top: 4px;
}

/* Каталог */
.bag-catalog {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
  background-color: #e0d8ce;
}
</style>