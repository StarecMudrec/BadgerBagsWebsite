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
      

      <!-- Delete Confirmation Dialog -->
      <!-- Update the confirmation dialog template in Home.vue -->
      <transition name="fade" @after-leave="resetDialog">
        <div v-if="showDeleteConfirmation" class="confirmation-dialog-overlay">
          <transition name="scale" @after-leave="handleDialogClose">
            <div v-if="showDialogContent" class="confirmation-dialog" :class="{ 'processing': isDeleting }">
              <div v-if="!isDeleting">
                <h3>Подтвердите удаление</h3>
                <p>Вы уверены, что хотите удалить выбранные товары? Это действие невозможно отменить.</p>
                <div class="dialog-buttons">
                  <button @click="confirmDelete" class="confirm-button" title="Delete">
                    <i class="bi bi-trash"></i>
                  </button>
                  <button @click="cancelDelete" class="cancel-button" title="Cancel">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </div>
              <div v-else class="deleting-state">
                <div class="deleting-spinner"></div>
                <div class="deleting-text">Deleting...</div>
              </div>
            </div>
          </transition>
        </div>
      </transition>

      <div v-if="loading">
        <div class="loading-container">
          <div class="spinner"></div>
          <div class="loading-text">Загрузка...</div>
        </div>
      </div>
      <div v-else class="bag-catalog">
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
              <div class="sort-option" @click="sortByNewest">Сначала новые</div>
              <div class="sort-option" @click="sortByOldest">Сначала старые</div>
            </div> 
          </transition>
          
          <!-- Add delete button -->
          <button 
            v-if="showDeleteButton" 
            @click="openConfirmation"
            class="delete-button"
            :disabled="isDeleting"
          >
            <span>
              <!-- {{ selectedBags.size }}  -->
              <i class="bi bi-trash"></i>
            </span>
          </button>
        </div>
        <transition-group 
          name="list" 
          tag="div" 
          class="bag-grid"
        >
          <BagCard 
            v-for="bag in sortedBags" 
            :key="'bag-' + bag.id"  
            :bag="bag" 
            :selection-mode="showDeleteButton"
            class="bag-item"
            :class="{ 
              'selected': selectedBags.has(bag.id),
              'no-hover': selectedBags.has(bag.id)
            }"
            data-test="bag-card"
            @bag-selected="handleBagSelected"
          />
          <div style=" display: flex; flex-direction: column; align-items: center;">
            <div class="add-item-button" @click="navigateToAddItem" data-test="add-item-button">
              <div class="add-item-inner">
                <svg class="plus-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 5V19M5 12H19" stroke="#423125" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
            <!-- <div data-v-db91d383="" class="bag-price unselectable" style="color: rgb(0, 0, 0, 0);">.</div> -->
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
import axios from 'axios'; // Add this import

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
      selectedBags: new Set(), // Track selected bags
      showDeleteButton: false, // Control delete button visibility
      showDeleteConfirmation: false,
      selectedSeasons: new Set(), // Track selected seasons
      isDeleting: false, // Add this line
      showDialogContent: false,
      closeAfterLoading: false
    };
  },
  computed: {
    sortedBags() {
      if (this.sortMethod === 'price-asc') {
        return [...this.bags].sort((a, b) => a.price - b.price);
      } else if (this.sortMethod === 'price-desc') {
        return [...this.bags].sort((a, b) => b.price - a.price);
      } else if (this.sortMethod === 'newest') {
        return [...this.bags].sort((a, b) => b.id - a.id); // Newest first (highest ID)
      } else if (this.sortMethod === 'oldest') {
        return [...this.bags].sort((a, b) => a.id - b.id); // Oldest first (lowest ID)
      }
      return this.bags;
    }
  },

  methods: {
    // Add these animation methods for selected state
    beforeEnter(el) {
      gsap.set(el, {
        opacity: 0,
        y: 30
      });
    },
    
    enter(el, done) {
      const delay = el.dataset.index * 0.1;
      const isSelected = this.selectedBags.has(el.__vnode.key.replace('bag-', ''));
      
      gsap.to(el, {
        opacity: 1,
        y: isSelected ? -15 : 0,
        duration: 0.5,
        delay: delay,
        ease: "back.out(1.7)",
        onComplete: done
      });
    },
    
    leave(el, done) {
      // First shrink and fade out the deleted card
      gsap.to(el, {
        scale: 0.8,
        opacity: 0,
        duration: 0.3,
        ease: "power2.in",
        onComplete: () => {
          // After card disappears, animate remaining cards
          this.$nextTick(() => {
            this.animateRemainingCards().then(done);
          });
        }
      });
    },
    
    afterEnter(el) {
      el.style.transform = '';
    },
    
    afterLeave() {
      // Cleanup if needed
    },
    
    async animateRemainingCards() {
      await this.$nextTick();
      const cards = document.querySelectorAll('.bag-item');
      
      cards.forEach((card, index) => {
        gsap.to(card, {
          x: 0,
          y: 0,
          duration: 0.5,
          delay: index * 0.05,
          ease: "back.out(1.7)"
        });
      });
      
      // Wait for animations to complete
      return new Promise(resolve => {
        setTimeout(resolve, 500 + (cards.length * 50));
      });
    },

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
    sortByNewest() {
      this.sortMethod = 'newest';
      this.showSortDropdown = false;
    },
    
    sortByOldest() {
      this.sortMethod = 'oldest';
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
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 0.5,
        ease: "back.out(1.7)",
        onComplete: done
      });
    },
    
    leave(el, done) {
      gsap.to(el, {
        scale: 0.8,
        opacity: 0,
        duration: 0.3,
        ease: "power2.in",
        onComplete: done
      });
    },
    afterEnter(el) {
      el.style.transform = '';
    },
    handleBagSelected(bagId, isSelected) {
      if (isSelected) {
        this.selectedBags.add(bagId);
        this.animateSelection(bagId, true);
      } else {
        this.selectedBags.delete(bagId);
        this.animateSelection(bagId, false);
      }
      this.showDeleteButton = this.selectedBags.size > 0;
    },
    
    openConfirmation() {
      this.showDeleteConfirmation = true;
      this.showDialogContent = true;
    },
    
    async confirmDelete() {
      try {
        this.isDeleting = true;
        const deletePromises = Array.from(this.selectedBags).map(bagId => 
          axios.delete(`/api/bags/${bagId}`, { withCredentials: true })
            .catch(error => {
              console.error(`Error deleting bag ${bagId}:`, error);
              throw error; // Re-throw to be caught by the outer catch
            })
        );
        
        await Promise.all(deletePromises);
        this.bags = this.bags.filter(bag => !this.selectedBags.has(bag.id));
        this.closeAfterLoading = true;
        this.showDialogContent = false;
      } catch (error) {
        console.error('Deletion error:', error);
        this.isDeleting = false;
        // Optionally show an error message to the user
      }
    },
    
    handleDialogClose() {
      if (this.closeAfterLoading) {
        this.resetDialog();
      }
    },
    
    resetDialog() {
      this.showDeleteConfirmation = false;
      this.isDeleting = false;
      if (this.closeAfterLoading) {
        this.selectedBags.clear();
        this.showDeleteButton = false;
      }
      this.closeAfterLoading = false;
      this.showDialogContent = false;
    },
  
    cancelDelete() {
      // Add a separate method for cancel to handle animation
      this.showDeleteConfirmation = false;
    },
    
    animateSelection(bagId, isSelected) {
      const element = document.querySelector(`[data-test="bag-card"][key="bag-${bagId}"]`);
      if (element) {
        gsap.to(element, {
          y: isSelected ? -15 : 0,
          duration: 0.3,
          ease: "back.out(1.7)",
          boxShadow: isSelected ? '0 10px 20px rgba(0,0,0,0.2)' : 'none'
        });
      }
    },
    
    async deleteSelectedBags() {
      try {
        // For testing, we'll just remove them from the local state
        // In a real app, you'd call an API endpoint here
        this.bags = this.bags.filter(bag => !this.selectedBags.has(bag.id));
        this.selectedBags.clear();
        this.showDeleteButton = false;
        
        // Optional: Show success message
        console.log('Bags deleted successfully');
      } catch (error) {
        console.error('Error deleting bags:', error);
      }
    },
  },

  async created() {
    const response = await fetch('/api/bags');
    try {
      this.bags = await response.json();
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

  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  /* Dialog scale transition */
  .scale-enter-active {
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }
  .scale-leave-active {
    transition: all 0.2s cubic-bezier(0.6, -0.28, 0.735, 0.045);
  }
  .scale-enter-from,
  .scale-leave-to {
    opacity: 0;
    transform: scale(0.95);
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
    position: fixed;
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
    /* background-color: white; */
    margin: 0;
    border: none;
  }

  .content {
    position: relative;
    width: 100%;
    min-height: 52vh;
    left: 0;
    top: 4px;
    flex: 1;
    background: linear-gradient(to bottom, #f0e9e100 0%, #e7e2dc 100%);
  }

  .sort-container {
    position: relative;
    margin-bottom: 20px;
    /* padding-top: 32px; */
    border-bottom: 1px solid #ffffffdb;
    padding-bottom: 10px;

  }

  .sort-icon {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 22px;
    height: 22px;
    margin-left: 7px;
    cursor: pointer;
    padding: 3px 0;
  }

  .sort-icon-line {
    display: block;
    height: 2px;
    background-color: #423125db;
    transition: all 0.3s ease;
    box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.2);
  }

  .sort-icon-line:nth-child(1) {
    width: 90%;
    border-radius: 2px;
  }

  .sort-icon-line:nth-child(2) {
    width: 60%;
    border-radius: 2px;
  }

  .sort-icon-line:nth-child(3) {
    width: 30%;
    border-radius: 2px;
  }

  .sort-icon:hover .sort-icon-line {
    opacity: 0.7;
  }

  .sort-dropdown {
    position: absolute;
    top: 100%;
    margin-top: 10px;
    left: 5px;
    background-color: #d3cdc5bf;
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
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  .sort-option:hover {
    background-color: #d3cdc5;
  }

  .sort-option:last-child {
    border-bottom: none;
  }

  .delete-button {
    position: fixed;
    bottom: 42px;
    right: 42px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    /* color: #ff4444; */
    background: none;
    color: #ff4444;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    font-size: 42px;
    cursor: pointer;
    text-shadow: 1px 2px 3px rgb(0 0 0 / 67%);
    transition: all 0.2s ease;
    z-index: 100;
  }

  .delete-button:hover {
    color: rgb(255, 76, 76);
    transform: translateY(-2px);
    transform: scale(1.02);
    /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25); */
  }



  /* Confirmation Dialog Styles */
  .confirmation-dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    backdrop-filter: blur(5px);
  }

  .confirmation-dialog {
    background-color: #f4ebe2;
    border-radius: 12px;
    padding: 22px;
    max-width: 400px;
    width: 90%;
    text-align: center;
    border: 1px solid #d0cbc4;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15); 
    transition: all 0.3s ease;
    transform-origin: center;
  }

  .confirmation-dialog h3 {
    margin-top: 0;
    color: #423125;
    font-weight: 700;
    margin-bottom: 15px;
    font-size: 1.5rem;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
  }

  .confirmation-dialog p {
    margin-bottom: 22px;
    color: #423125;
    line-height: 1.5;
    font-size: 1.1rem;
  }

  .dialog-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
  }

  .confirm-button, .cancel-button {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    border: none;
    background-color: rgba(0, 0, 0, 0.2);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1.5rem;
    backdrop-filter: blur(5px);
  }

  .confirm-button:hover {
    background-color: rgba(210, 43, 43, 0.8);
    transform: scale(1.1);
  }

  .cancel-button:hover {
    background-color: rgba(66, 49, 37, 0.8);
    transform: scale(1.1);
  }

  .confirm-button i, .cancel-button i {
    color: rgba(255, 255, 255, 0.9);
  }

  /* Add these styles to the existing confirmation dialog styles */
  .confirmation-dialog.processing {
    background-color: rgba(244, 235, 226, 0);
    /* backdrop-filter: blur(2px); */
    border: none;
    box-shadow: none;
    transition: all 0.3s ease, background-color 0.1s ease;
  }

  .deleting-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    transition: all 0.3s ease;
  }

  .deleting-spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(66, 49, 37, 0.2);
    border-top-color: #f3eee8;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
  }

  .deleting-text {
    color: #f3eee8;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 1px;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Add these icon classes if not already present */
  /* .bi-trash {
    display: inline-block;
    width: 1em;
    height: 1em;
    vertical-align: middle;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' viewBox='0 0 16 16'%3E%3Cpath d='M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z'/%3E%3Cpath fill-rule='evenodd' d='M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-size: contain;
  } */

  .loading-container {
    position: absolute;
    /* top: 50%; */
    margin-top: 50px;
    left: 50%;
    transform: translate(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .loading-text {
    font-weight: 600;
    font-size: 2rem;
    color: #423125;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 5px solid rgba(66, 49, 37, 0.2); /* Light brown with opacity */
    border-top-color: #423125; /* Dark brown */
    border-radius: 50%;
    animation: spin 1s ease-in-out infinite; /* Changed from linear to ease-in-out */
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .bag-catalog {
    /* width: 100%; */
    padding: 25px;
    border-radius: 8px;
    border: 0.5px solid #f8f3ed;
    max-width: 1450px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 30px;
    margin-bottom: 30px;
    background-color: #f3eee8;
    box-shadow: 2px 4px 5px rgba(0, 0, 0, 0.24);
  }

  .bag-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(174px, 1fr));
    grid-auto-rows: 1fr; /* Ensures all rows are equal height */
    gap: 20px;
    column-gap: 50px;
    width: 100%;
    /* padding: 20px; */
    position: relative;
    /* Remove align-items: stretch */
    perspective: 1000px; /* Adds depth for smoother 3D effects */ 
    padding-left: 30px;
    padding-right: 30px;
  }

  /* Enhance the transition effects */
  .list-enter-active,
  .list-leave-active,
  .list-move {
    transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
  }

  .list-enter-from,
  .list-leave-to {
    opacity: 0;
    transform: translateY(30px);
  }

  /* Add these styles */
  .list-move {
    transition: transform 0.5s ease;
  }

  .list-enter-active,
  .list-leave-active {
    transition: all 0.5s;
  }

  .list-enter-from {
    opacity: 0;
    transform: translateY(30px);
  }

  .list-leave-to {
    opacity: 0;
    transform: scale(0.8);
  }

  .list-leave-active {
    position: absolute;
    width: calc(100% / var(--columns, 4) - 20px);
    /* Adjust --columns based on your grid layout */
  }

  .bag-item, .add-item-button {
    display: flex;
    flex-direction: column;
    /* min-height: 100%; Ensure they take full height */
  }

  .bag-item {
    display: flex;
    flex-direction: column;
    /* Add aspect ratio to maintain consistent sizing */
    aspect-ratio: 1 / 1.78; 
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border-radius: 4px;
  }

  .bag-item.selected {
    transform: translateY(-15px);
    z-index: 10;
    position: relative;
  }

  /* Add this new rule to disable hover on selected cards */
  .bag-item.no-hover:hover {
    transform: translateY(-15px) !important; /* Maintain raised position */
    filter: brightness(1.05) contrast(1.05);
  }

  .bag-item:not(.selected):hover {
    transform: translateY(-5px); /* Only apply hover effect to non-selected cards */
    filter: brightness(1.05) contrast(1.05);
  }

  .bag-item >>> .bag-card {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .bag-item >>> .bag-image-container {
    flex-grow: 1;
    position: relative;
  }

  .bag-item >>> .bag-image {
    width: 100%;
    /* height: 100%; */
    object-fit: cover;
  }

  /* Animation styles */
  .list-item {
    transition: all 0.5s ease;
    will-change: transform, opacity;
  }

  .unselectable {
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
    user-select: none; /* Standard */
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

  /* .bag-catalog >>> .bag-card .bag-image:hover {
    transform: translateY(-5px);
    filter: brightness(1.05) contrast(1.05);
  } */

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
    flex-direction: column;
    border: 2px dashed #423125;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    background-color: rgba(255, 255, 255, 0.05);
    width: 100%;
    position: relative;
    overflow: hidden;
    height: 100%;
    /* aspect-ratio: 1 / 1.56630057630; */
    /* margin-bottom: 10px; */ 
    min-height: 50px;
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
    position: absolute; /* Fill the container */
    top: 0;
    left: 0;
  }

  .plus-icon {
    width: 50px;
    height: 50px;
    transition: all 0.3s ease;
  }

  .add-item-button:hover .plus-icon {
    transform: scale(1.1);
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

  @media (max-width: 768px) {
    .bag-grid {
      padding-left: 0px;
      padding-right: 0px;
    }
    .bag-catalog[data-v-2dc54a20] {
        margin-left: 10px;
        margin-right: 10px;
    }
    .add-item-button {
      height: 50px;      
    }
  }

  @media (max-width: 1550px) {
    .bag-catalog {
      margin-left: 50px;
      margin-right: 50px;
    }
  }
</style>