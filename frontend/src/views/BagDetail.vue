<template>
  <div class="bag-detail-page">
    <!-- Image Section (40% width, full height) -->
    <div class="image-section" @wheel="handleWheel">
      <div class="arrow-nav left" @click="prevImage">
        <div class="arrow-inner">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 18l-6-6 6-6"/>
          </svg>
        </div>
      </div>
      
      <img :src="currentImage" :alt="bag.name" class="bag-image" />
      
      <div class="arrow-nav right" @click="nextImage">
        <div class="arrow-inner">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18l6-6-6-6"/>
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

/* Arrow Navigation - Horizontal */
.arrow-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  z-index: 10;
  width: 60px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.arrow-nav:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: translateY(-50%) scale(1.05);
}

.arrow-nav.left {
  left: 30px;
}

.arrow-nav.right {
  right: 30px;
}

.arrow-icon {
  width: 24px;
  height: 24px;
  stroke: #423125;
  stroke-width: 2;
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
  font-weight: 500;
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

/* iOS-style glass button */
.buy-button {
  display: inline-block;
  padding: 15px 30px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #423125;
  text-decoration: none;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 600;
  font-size: 1.5rem;
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
    width: 50px;
    height: 50px;
  }
  
  .arrow-nav.left {
    left: 15px;
  }
  
  .arrow-nav.right {
    right: 15px;
  }
  
  .buy-button {
    padding: 12px 24px;
    font-size: 1.2rem;
  }
}
</style>