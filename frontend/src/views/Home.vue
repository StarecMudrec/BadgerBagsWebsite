<template>
  <!-- Фон (прижат к самому верху) -->
  <div class="background-wrapper">
    <div class="background-container"></div>
  </div>
  
  <!-- Линия-разделитель -->
  <hr class="separator-line" />
  
  <!-- Основной контент -->
  <div class="content">
    <div class="sort-container">
      <button class="sort-button" @click="toggleSortDropdown">Sort</button>
      <transition name="sort-dropdown">
        <div class="sort-dropdown" v-if="showSortDropdown">
          <div class="sort-option" @click="sortByPriceAscending">Price: Low to High</div>
          <div class="sort-option" @click="sortByPriceDescending">Price: High to Low</div>
          <div class="sort-option">Newest</div>
        </div> 
      </transition>
    </div>


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
      bags: [],
      showSortDropdown: false, // Data property to control dropdown visibility
    };
  },

  methods: {
    toggleSortDropdown() {
      this.showSortDropdown = !this.showSortDropdown;
    },
    sortByPriceAscending() {
      this.bags.sort((a, b) => a.price - b.price);
      this.showSortDropdown = false;
    },
    sortByPriceDescending() {
      this.bags.sort((a, b) => b.price - a.price);
      this.showSortDropdown = false;
    },
    // Add sortByNewest method here later if needed bag

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
  background-color: #e0d8ce;
}

/* Стили для контейнера сортировки */
.sort-container {
  position: relative; /* Для позиционирования выпадающего списка */
  margin-bottom: 20px; /* Отступ перед каталогом */
  padding-top: 20px; /* Отступ сверху */
}

/* Стили для кнопки сортировки */
.sort-button {
  background-color: #423125;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  margin-left: 40px; /* Отступ слева */
  border-radius: 5px;
}

/* Стили для выпадающего списка */
.sort-dropdown {
  position: absolute;
  top: 100%; /* Располагаем под кнопкой */
  left: 40px; /* Совпадаем по левому краю с кнопкой */
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10; /* Убедимся, что выпадающий список поверх другого контента */
  min-width: 150px; /* Минимальная ширина выпадающего списка */
  border-radius: 5px;
}

/* Каталог */
.bag-catalog {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;

}.sort-option {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}
</style>

<style scoped>
/* Animations for the sort dropdown */
.sort-dropdown-enter-active, .sort-dropdown-leave-active {
  transition: opacity 0.3s ease, max-height 0.3s ease;
  overflow: hidden;
}

.sort-dropdown-enter, .sort-dropdown-leave-to {
  opacity: 0;
  max-height: 0;
}

.sort-dropdown-enter-to, .sort-dropdown-leave {
  opacity: 1;
  max-height: 200px; /* Adjust based on the maximum possible height of your dropdown */
}
</style>