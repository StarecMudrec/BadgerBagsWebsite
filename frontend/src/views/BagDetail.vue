<template>
  <div class="bag-detail-page" v-if="!loading && !error">
    <!-- Image Section -->
    <div class="image-section" @wheel="handleWheel" v-if="bag">
      <div class="arrow-nav left" @click="prevImage">
        <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="6 6 12 12" width="36" height="36">
          <!-- SVG content remains the same -->
        </svg>
      </div>
      
      <img :src="currentImage" :alt="bag?.name" class="bag-image" v-if="bag?.img" />
      
      <div class="arrow-nav right" @click="nextImage">
        <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="6 6 12 12" width="36" height="36">
          <!-- SVG content remains the same -->
        </svg>
      </div>
    </div>

    <!-- Text Section (60% width) -->
    <div class="text-section" v-if="bag">
      <div class="text-content">
        <h2 class="section-title">О сумке:</h2>
        <p class="section-text">{{ bag?.description || 'Здесь будет находиться информация о сумке' }}</p>
        
        <div class="price-section">
            <div class="price">{{ bag?.price }}₽</div>
            <a href="https://t.me/kurorooooo" class="buy-button" target="_blank">
                <span class="button-text">КУПИТЬ</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" class="telegram-icon">
                    <!-- SVG path remains the same -->
                </svg>
            </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Loading and Error States -->
  <div v-if="loading" class="loading-state">
    Loading bag details...
  </div>
  
  <div v-if="error" class="error-state">
    {{ error }}
  </div>
</template>

<script>
export default {
  props: {
    id: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      bag: null,
      error: null,
      loading: false,
      currentImage: ''
    }
  },
  methods: {
    async fetchBagDetails() {
      this.loading = true;
      this.error = null;
      this.bag = null;
      
      try {
        const response = await fetch(`/api/bags/${this.id}`);
        
        if (!response.ok) {
          throw new Error(response.status === 404 
            ? 'Bag not found' 
            : 'Failed to fetch bag details');
        }
        
        this.bag = await response.json();
        this.currentImage = this.bag?.img ? `/bags_imgs/${this.bag.img}` : '';
      } catch (err) {
        this.error = err.message;
        console.error('Error:', err);
        
        if (err.message.includes('not found')) {
          this.$router.replace('/404');
        }
      } finally {
        this.loading = false;
      }
    },
    prevImage() {
      // Implement if you have multiple images
    },
    nextImage() {
      // Implement if you have multiple images
    },
    handleWheel(e) {
      // Implement wheel handling if needed
    }
  },
  mounted() {
    if (this.id && this.id !== 'undefined') {
      this.fetchBagDetails();
    } else {
      this.error = 'Invalid bag ID';
    }
  },
  watch: {
    id(newId) {
      if (newId && newId !== 'undefined') {
        this.fetchBagDetails();
      }
    }
  }
}
</script>

<style scoped>
.loading-state,
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-size: 1.5rem;
  color: #423125;
}

.error-state {
  color: #d32f2f;
}

@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700;900&family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

.bag-detail-page {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* Image Section (40% width, full height) */
.image-section {
  width: 40%;
  height: 100vh;
  position: relative;
  background-color: #f4ebe2;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* Add this to contain the image */
}

.bag-image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* This maintains aspect ratio while filling space */
  object-position: center; /* Ensures image is centered */
  min-width: 0; /* Allows proper flex behavior */
  min-height: 0; /* Allows proper flex behavior */
}

/* Arrow Navigation - Horizontal */
.arrow-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  z-index: 10;
  width: 52px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.arrow-nav.left {
  left: 20px;
}

.arrow-nav.right {
  right: 20px;
}

.arrow-inner {
  width: 48px; /* Match SVG width */
  height: 48px; /* Match SVG height */
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
  pointer-events: none;
}

.arrow-path {
  transition: fill 0.3s ease;
  transform-origin: center;
}

.arrow-nav:hover .arrow-icon {
  transform: scale(0.85);
  opacity: 0.9;
}

.arrow-nav:hover .arrow-inner {
  animation-play-state: paused;
}
/* 
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
} */

/* Text Section (60% width) */
.text-section {
  width: 60%;
  padding: 40px 10% 40px 12%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
}

.text-content {
  width: 100%;
  max-width: 700px;
}

.section-title {
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 1000;
  font-size: 3rem;
  color: #423125;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 1px solid #a69d96;
  width: 100%;
  letter-spacing: 0.5px;
}

.section-text {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 700;
  font-size: 1.8rem;
  line-height: 1.3;
  color: #423125;
  letter-spacing: 0.2px;
  margin-bottom: 40px;
}

.price-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 40px;
}

.price {
  font-family: 'Aclonica', sans-serif;
  font-size: 2.5rem;
  color: #333333;
}

.buy-button {
    display: inline-block;
    padding: 9px 17px;
    padding-top: 5px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #333333;
    text-decoration: none;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-size: 1.5rem;    
    font-weight: 1000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    /* gap: 8px; Add space between text and icon */
}

.buy-button:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.buy-button:active {
  transform: translateY(0);
}

/* Optional: Add a subtle gradient to the button */
.buy-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 100%);
  border-radius: 8px;
  z-index: -1;
}

.button-text {
  display: inline-block;
  vertical-align: middle;
}

.telegram-icon {
  width: 27px;
  height: 27px;
  transition: all 0.3s ease;
  fill: #333333;
  vertical-align: middle;
  margin-left: 7px;   
}

@media (max-width: 768px) {
  .bag-detail-page {
    flex-direction: column;
    height: auto;
  }
  
  .image-section {
    width: 100%;
    height: auto; /* Changed to auto to match image height */
    min-height: 50vh; /* Fallback minimum height */
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 2px solid #ffffff;
  }
  
  .bag-image {
    width: 100%;
    height: auto;
    /* max-height: 100vh; */
    object-fit: contain;
  }
  
  .text-section {
    width: 100%;
    padding: 30px 20px;
    padding-top: 10px;
  }
  
  .section-title {
    font-size: 2.4rem;
    margin-top: 0px;
  }
  
  .section-text {
    font-size: 1.5rem;
  }
  
  .arrow-nav {
    width: 28px;
    height: 28px;
    padding: 14px;
  }
  
  .arrow-nav.left {
    left: 10px;
  }
  
  .arrow-nav.right {
    right: 10px;
  }
}
</style>