<template>
  <!-- Фон (прижат к самому верху) -->
  <div class="background-wrapper">
    <div class="background-container"></div>
    <!-- Стрелка для скролла -->
    <h1 class="title">Badger bags</h1>
    <div class="cover-arrow" @click="scrollToContent">
      <div class="cover-arrow__inner">
        <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="7.5 11 9 4" fill="white" width="24px" height="24px">
          <defs>
            <!-- Fading shadow filter -->
            <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
              <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
              <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
            </filter>
          </defs>
          <path class="arrow-path" fill="white"  filter="url(#arrowShadow)" d="M9 11l3 3 3-3c.2-.2.5-.2.7 0 .2.2.2.5 0 .7l-3.5 3.5c-.2.2-.5.2-.7 0L8.3 11.7c-.2-.2-.2-.5 0-.7.2-.2.5-.2.7 0z"/>
        </svg>
      </div>
    </div>
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
    scrollToContent() {
      const contentSection = document.querySelector('.content');
      if (contentSection) {
        contentSection.scrollIntoView({ behavior: 'smooth' });
      }
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
@import url('https://fonts.googleapis.com/css2?family=BIZ+UDPMincho&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap');
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

.title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 7rem;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 200;
  text-align: center;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
  margin: 0;
  z-index: 1;
  width: 100%;
}

/* Сам фон */
.background-container { 
  position: fixed;
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
  min-height: calc(100vh - 0px);
  left: 0;
  top: 4px;
  background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
}

/* Стили для контейнера сортировки */
.sort-container {
  position: relative;
  margin-bottom: -20px;
  padding-top: 32px;
}

/* Стили для иконки сортировки (гамбургер) */
.sort-icon {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 30px;
  margin-left: 52px;
  cursor: pointer;
  padding: 3px 0;
}

.sort-icon-line {
  display: block;
  height: 3px;
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
  opacity: 0.7;
}

/* Стили для выпадающего списка */
.sort-dropdown {
  position: absolute;
  top: 100%;
  margin-top: 10px;
  left: 40px;
  background-color: #cdc5bccf;
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
  font-weight: 500;
  font-size: 1.15rem;
  /* font-family: 'Noto Serif TC', 'Noto Serif', serif; */
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

/* New styles for the arrow button */
.cover-arrow {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  z-index: 2;
}

.cover-arrow__inner {
  animation: bounce 2s infinite;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 85px;
  height: 67px;
  /* background-color: rgba(255, 255, 255, 0.2); */
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.arrow-icon {
  width: 100%;
  height: 100%;
  shape-rendering: geometricPrecision;
  transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
  pointer-events: bounding-box; /* Only detect hovers on visible shape */
}

.arrow-icon:hover {
  transform: scale(0.85);
  opacity: 0.9;
  transition: all 0.2s ease;
}

.arrow-icon:hover ~ .cover-arrow__inner,
.arrow-icon:hover {
  animation-play-state: paused;
}

.arrow-path {
  transition: fill 0.3s ease;
  transform-origin: center;
  pointer-events: visible; /* Only respond to hovers on visible pixels */
}

/* .cover-arrow svg {
  width: 170px;
  height: 170px;
  shape-rendering: geometricPrecision;
  transition: all 0.3s ease;
  will-change: transform;
} */

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>