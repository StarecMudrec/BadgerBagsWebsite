<template>
  <div class="page-container">
    <!-- Фон (прижат к самому верху) -->
    <div class="hero-section">
      <div class="background-container"></div>
      <h1 class="title">Badger bags</h1>
      <div class="cover-arrow" @click="scrollToContent">
        <div class="cover-arrow__inner">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="7.5 11 9 4" fill="white" width="24px" height="24px">
            <defs>
              <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
                <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
              </filter>
            </defs>
            <path class="arrow-path" fill="white" filter="url(#arrowShadow)" d="M9 11l3 3 3-3c.2-.2.5-.2.7 0 .2.2.2.5 0 .7l-3.5 3.5c-.2.2-.5.2-.7 0L8.3 11.7c-.2-.2-.2-.5 0-.7.2-.2.5-.2.7 0z"/>
          </svg>
        </div>
      </div>
    </div>
    
    <!-- Линия-разделитель -->
    <hr class="separator-line" />
    
    <!-- Основной контент -->
    <div id="content-section" class="content">
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
        <transition-group 
          name="list" 
          tag="div" 
          class="bag-grid"
          @before-enter="beforeEnter"
          @enter="enter"
          @leave="leave"
        >
          <BagCard 
            v-for="bag in sortedBags" 
            :key="'bag-' + bag.id"  
            :bag="bag" 
            class="bag-item"
            data-test="bag-card"
          />
          <div class="add-item-button" @click="navigateToAddCard">
            <div class="add-item-inner">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
    <nav class="bottom-navbar">
      <router-link to="/about" class="navbar-button" style="text-decoration: none;">О НАС</router-link>
      <a href="https://t.me/kurorooooo" class="navbar-button telegram-button" style="text-decoration: none;" target="_blank">
        ТЕЛЕГРАМ
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" class="telegram-icon">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
        </svg>
      </a>
    </nav>
  </div>
</template>

<script>
import BagCard from '@/components/BagCard.vue';
import { gsap } from 'gsap';

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
    BagCard,
  },

  directives: {
    'click-outside': clickOutside
  },

  data() {
    return {
      bags: [],
      showSortDropdown: false,
      loading: true,
      sortMethod: 'default',
    };
  },
  computed: {
    sortedBags() {
      if (this.sortMethod === 'price-asc') {
        return [...this.bags].sort((a, b) => a.price - b.price);
      } else if (this.sortMethod === 'price-desc') {
        return [...this.bags].sort((a, b) => b.price - a.price);
      }
      return this.bags;
    }
  },

  methods: {
    toggleSortDropdown() {
      this.showSortDropdown = !this.showSortDropdown;
    },
    closeSortDropdown() {
      this.showSortDropdown = false;
    },
    sortByPriceAscending() {
      this.sortMethod = 'price-asc';
      this.showSortDropdown = false;
    },
    sortByPriceDescending() {
      this.sortMethod = 'price-desc';
      this.showSortDropdown = false;
    },
    navigateToAddItem() {
      this.$router.push('/add-item');
    },
    scrollToContent() {
      const contentSection = document.querySelector('.content');
      if (contentSection) {
        contentSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start'
        });
      }
    },
    // Animation methods
    beforeEnter(el) {
      gsap.set(el, {
        opacity: 0,
        y: 30
      });
    },
    
    enter(el, done) {
      console.log('Animating element:', el, 'with key:', el.__vnode.key);
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 0.5,
        ease: "power2.out",
        onComplete: done
      });
    },
    
    leave(el, done) {
      gsap.to(el, {
        opacity: 0,
        y: -30,
        duration: 0.3,
        ease: "power2.in",
        onComplete: done
      });
    },
    afterEnter(el) {
      el.style.transform = '';
    },
  },

  async created() {
    const response = await fetch('/api/bags');
    try {
      this.bags = await response.json();
      // Ensure each bag has an ID
      this.bags = this.bags.map((bag, index) => ({ ...bag, id: bag.id || index }));
      console.log('Bags data:', this.bags);
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=BIZ+UDPMincho&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap');

body, html, #app {
  margin: 0 !important;
  padding: 0 !important;
}

.page-container {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero-section {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
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

.background-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%;
  z-index: -1;
}

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

.content {
  position: relative;
  width: 100%;
  min-height: calc(100vh - 67px);
  left: 0;
  top: 4px;
  flex: 1;
  background: linear-gradient(to bottom, #f3efeb 0%, #e7e2dc 100%);
}

.sort-container {
  position: relative;
  margin-bottom: -20px;
  padding-top: 32px;
}

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
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.2);
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
}

.sort-option:hover {
  background-color: #dbd5cf;
}

.sort-option:last-child {
  border-bottom: none;
}

.bag-catalog {
  width: 100%;
  padding: 20px;
}

.bag-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  width: 100%;
  padding: 20px;
  position: relative;
}

/* Animation styles */
.list-item {
  transition: all 0.5s ease;
  will-change: transform, opacity;
}

/* .list-enter-active,
.list-leave-active,
.list-enter-from,
.list-leave-to {
  
} */

.list-move {
  transition: transform 0.5s ease;
}

.bag-catalog >>> .bag-card {
  transition: transform 0.3s ease;
}

.bag-catalog >>> .bag-card .bag-image {
  transition: all 0.3s ease;
  transform: translateY(0);
}

.bag-catalog >>> .bag-card .bag-image:hover {
  transform: translateY(-5px);
  filter: brightness(1.05) contrast(1.05);
}

.bag-catalog >>> .bag-card .bag-image:hover::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  pointer-events: none;
  border-radius: inherit;
}

.add-item-button {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px dashed #423125;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: rgba(255, 255, 255, 0.1);
  min-height: 300px; /* Adjust to match your card height */
}

.add-item-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
}

.add-item-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
}

.add-item-button svg {
  width: 40px;
  height: 40px;
  stroke: #423125;
  transition: all 0.3s ease;
}

.add-item-button:hover svg {
  transform: scale(1.1);
  stroke: #000;
}

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

.cover-arrow {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  z-index: 10;
  width: 85px;
  height: 67px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-arrow__inner {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: bounce 2s infinite;
}

.arrow-icon {
  width: 100%;
  height: 100%;
  shape-rendering: geometricPrecision;
  transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
  pointer-events: none;
}

.cover-arrow:hover .arrow-icon {
  transform: scale(0.85);
  opacity: 0.9;
}

.cover-arrow:hover .cover-arrow__inner {
  animation-play-state: paused;
}

.arrow-path {
  transition: fill 0.3s ease;
  transform-origin: center;
}

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

.page-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.bottom-navbar {
  width: 100%;
  background: linear-gradient(to bottom, #dad4ce 0%, #d0cbc4 100%);;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  margin-top: auto;
  min-height: 71px;
}

.navbar-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 1000;
  font-size: 22px;
  transition: color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  position: relative;
}

.navbar-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px #a69d96;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}

.navbar-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #a69d96;
  transition: width 0.3s ease;
  bottom: 5px;
}

.navbar-button:hover::after {
  width: 100%;
}

.telegram-button {
  display: flex;
  align-items: center;
  gap: 10px;
  position: relative;
}

.telegram-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px #a69d96;
}

.telegram-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #a69d96;
  transition: width 0.3s ease;
  bottom: 5px;
}

.telegram-button:hover::after {
  width: 100%;
}

.telegram-button:hover .telegram-icon {
  fill: var(--hover-color);
  transform: scale(1.1);
}

.telegram-button .telegram-icon {
  width: 27px;
  height: 27px;
  transition: all 0.3s ease;
  fill: #333333;
}
</style>