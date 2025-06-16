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
      <div class="sort-icon" @click.stop="toggleSortDropdown">
        <span class="sort-icon-line"></span>
        <span class="sort-icon-line"></span>
        <span class="sort-icon-line"></span>
      </div>
      <transition name="sort-dropdown">
        <div class="sort-dropdown" v-if="showSortDropdown" v-click-outside="closeSortDropdown">
          <div class="sort-option" @click="sortByPriceAscending">Сначала дешевле</div>
          <div class="sort-option" @click="sortByPriceDescending">Сначала дороже</div>
          <div class="sort-option">Сначала новые</div>
        </div> 
      </transition>
    </div>

    <div v-if="loading">Loading bags...</div>
    <div v-else class="bag-catalog">
      <BagCard v-for="bag in bags" :key="bag.id" :bag="bag" />
    </div>
  </div>
</template>

<script>
import BagCard from '@/components/BagCard.vue';

// Директива для обработки кликов вне элемента
const clickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value();
      }
    };
    document.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent);
  },
};

export default {
  components: {
    BagCard
  },

  directives: {
    'click-outside': clickOutside
  },

  data() {
    return {
      bags: [],
      showSortDropdown: false,
      loading: true,
    };
  },

  methods: {
    toggleSortDropdown() {
      this.showSortDropdown = !this.showSortDropdown;
    },
    closeSortDropdown() {
      this.showSortDropdown = false;
    },
    sortByPriceAscending() {
      this.bags.sort((a, b) => a.price - b.price);
      this.showSortDropdown = false;
    },
    sortByPriceDescending() {
      this.bags.sort((a, b) => b.price - a.price);
      this.showSortDropdown = false;
    },
  },

  async created() {
    const response = await fetch('/api/bags');
    try {
      this.bags = await response.json();
    } finally {
      this.loading = false;
    }
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
  background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
}

/* Стили для контейнера сортировки */
.sort-container {
  position: relative;
  margin-bottom: -20px;
  padding-top: 20px;
}

/* Стили для иконки сортировки (гамбургер) */
.sort-icon {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 20px;
  height: 20px;
  margin-left: 40px;
  cursor: pointer;
  padding: 2px 0;
}

.sort-icon-line {
  display: block;
  height: 2px;
  background-color: #423125;
  transition: all 0.3s ease;
}

.sort-icon-line:nth-child(1) {
  width: 100%;
  border-radius: 2px;
}

.sort-icon-line:nth-child(2) {
  width: 65%;
  border-radius: 2px;
}

.sort-icon-line:nth-child(3) {
  width: 35%;
  border-radius: 2px;
}

.sort-icon:hover .sort-icon-line {
  opacity: 0.8;
}

/* Стили для выпадающего списка */
.sort-dropdown {
  position: absolute;
  top: 100%;
  margin-top: 10px;
  left: 40px;
  background-color: #cdc5bccf;
  /* border: 1px solid #b5ada5; */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
  min-width: 100px;
  border-radius: 4px;
  overflow: hidden;
  will-change: transform, opacity;
  transform-origin: top center;
  color: #423125;
}

.sort-option {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  /* border-bottom: 1px solid #b5ada5; */
  font-weight: 700;
}

.sort-option:hover {
  background-color: #f5f5f5;
}

.sort-option:last-child {
  border-bottom: none;
}

/* Каталог */
.bag-catalog {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
}

/* Animations for the sort dropdown */
.sort-dropdown-enter-active {
  transition: all 0.3s ease-out;
}

.sort-dropdown-leave-active {
  transition: all 0.2s ease-in 0.1s;
}

.sort-dropdown-enter-from,
.sort-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.sort-dropdown-enter-to,
.sort-dropdown-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>