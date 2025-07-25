<template>
  <div class="bag-detail-page">
    <!-- Image Section (40% width, full height) -->
    <div class="image-section" @wheel="handleWheel">
      <div class="arrow-nav left" @click="prevImage">
        <div class="arrow-inner">
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
      
      <img :src="currentImage" :alt="bag.name" class="bag-image" />
      
      <div class="arrow-nav right" @click="nextImage">
        <div class="arrow-inner">
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

    <!-- Text Section (60% width) -->
    <div class="text-section">
      <div class="text-content">
        <h2 class="section-title">О сумке:</h2>
        <p class="section-text">{{ bag.description || 'Здесь будет находиться информация о сумке' }}</p>
        
        <div class="price-section">
          <div class="price">{{ bag.price }}₽</div>
          <a href="https://t.me/kurorooooo" class="buy-button" target="_blank">
            Купить ✅
          </a>
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

/* Arrow Navigation */
.arrow-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  z-index: 10;
  width: 85px;
  height: 67px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.arrow-nav.left {
  left: 30px;
}

.arrow-nav.right {
  right: 30px;
  transform: translateY(-50%) rotate(180deg);
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
  color: #423125;
}

.buy-button {
  display: inline-block;
  padding: 15px 30px;
  background-color: #423125;
  color: white;
  text-decoration: none;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-size: 1.5rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.buy-button:hover {
  background-color: #5a4a3a;
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