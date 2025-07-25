<template>
  <div class="bag-detail-page">
    <!-- Image Section (40% width, full height) -->
    <div class="image-section" @wheel="handleWheel">
      <div class="arrow-nav left" @click="prevImage">
        <div class="arrow-inner">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24px" height="24px">
            <defs>
              <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
                <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
              </filter>
            </defs>
            <path class="arrow-path" fill="white" filter="url(#arrowShadow)" d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/>
          </svg>
        </div>
      </div>
      
      <img :src="currentImage" :alt="bag.name" class="bag-image" />
      
      <div class="arrow-nav right" @click="nextImage">
        <div class="arrow-inner">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="24px" height="24px">
            <defs>
              <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
                <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
              </filter>
            </defs>
            <path class="arrow-path" fill="white" filter="url(#arrowShadow)" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Text Section (60% width) -->
    <div class="text-section">
      <div class="text-content">
        <h2 class="section-title">О сумке:</h2>
        <p class="section-text">{{ bag.description || 'Здесь будет находиться информация о сумке' }}</p>
        
        <div class="price-section">
          <div class="price">{{ bag.price }}₽</div>
          <div href="https://t.me/kurorooooo" class="buy-button" target="_blank">
            <a>
                КУПИТЬ
            </a>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" class="telegram-icon">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BagDetail',
  data() {
    return {
      bag: {},
      images: [], // Array of image URLs
      currentImageIndex: 0
    }
  },
  computed: {
    currentImage() {
      return this.images.length > 0 ? this.images[this.currentImageIndex] : '/placeholder.jpg';
    }
  },
  methods: {
    async fetchBagDetails() {
      try {
        const response = await fetch(`/api/bags/${this.$route.params.id}`);
        this.bag = await response.json();
        // For now, we'll just use the main image, but you can expand this to multiple images
        this.images = [this.bag.image ? `/bags_imgs/${this.bag.image}` : '/placeholder.jpg'];
      } catch (error) {
        console.error('Error fetching bag details:', error);
      }
    },
    nextImage() {
      this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length;
    },
    prevImage() {
      this.currentImageIndex = (this.currentImageIndex - 1 + this.images.length) % this.images.length;
    },
    handleWheel(event) {
      if (event.deltaY > 0) {
        this.nextImage();
      } else {
        this.prevImage();
      }
    }
  },
  mounted() {
    this.fetchBagDetails();
  }
}
</script>

<style scoped>
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
}

.bag-image {
  max-height: 100vh;
  max-width: 100%;
  object-fit: contain;
}

/* Arrow Navigation - Horizontal */
.arrow-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  z-index: 10;
  width: 120px; /* Doubled from 60px (original was 85px, then 90px) */
  height: 96px; /* Doubled from 48px (original was 67px, then 72px) */
  display: flex;
  justify-content: center;
  align-items: center;
}

.arrow-nav.left {
  left: 30px;
}

.arrow-nav.right {
  right: 30px;
  /* Remove the rotation transform since we're using proper left/right arrows now */
  transform: translateY(-50%);
}

.arrow-inner {
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
  line-height: 1.7;
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
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.25);
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

.telegram-icon {
  width: 27px;
  height: 27px;
  transition: all 0.3s ease;
  fill: #333333;
}

@media (max-width: 768px) {
  .bag-detail-page {
    flex-direction: column;
    height: auto;
  }
  
  .image-section {
    width: 100%;
    height: 50vh;
  }
  
  .text-section {
    width: 100%;
    padding: 30px 20px;
  }
  
  .section-title {
    font-size: 2.4rem;
  }
  
  .section-text {
    font-size: 1.5rem;
  }
  
  .arrow-nav {
    width: 60px;
    height: 50px;
  }
  
  .arrow-nav.left {
    left: 15px;
  }
  
  .arrow-nav.right {
    right: 15px;
  }
}
</style>