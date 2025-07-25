<template>
  <div class="bag-detail-container">
    <!-- Image Gallery Section -->
    <div class="image-gallery">
      <button class="nav-arrow left" @click="prevImage">←</button>
      <div class="image-container">
        <img :src="currentImage" :alt="bag.name" class="main-image" />
      </div>
      <button class="nav-arrow right" @click="nextImage">→</button>
    </div>
    
    <!-- Product Info Section -->
    <div class="product-info">
      <h1 class="product-title">{{ bag.name }}</h1>
      <p class="product-description">{{ bag.description }}</p>
      <div class="product-price">{{ bag.price }}₽</div>
      <a href="https://t.me/kurorooooo" class="buy-button" target="_blank">Купить ✅</a>
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
      return this.images.length > 0 ? this.images[this.currentImageIndex] : '';
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
    // Add wheel event listener for image navigation
    const gallery = document.querySelector('.image-container');
    if (gallery) {
      gallery.addEventListener('wheel', this.handleWheel);
    }
  },
  beforeDestroy() {
    // Clean up event listener
    const gallery = document.querySelector('.image-container');
    if (gallery) {
      gallery.removeEventListener('wheel', this.handleWheel);
    }
  }
}
</script>

<style scoped>
.bag-detail-container {
  display: flex;
  min-height: 100vh;
  padding: 40px;
  background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
}

.image-gallery {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 20px;
}

.image-container {
  width: 80%;
  height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.nav-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.5);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
}

.nav-arrow:hover {
  background: rgba(255, 255, 255, 0.8);
}

.nav-arrow.left {
  left: 20px;
}

.nav-arrow.right {
  right: 20px;
}

.product-info {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.product-title {
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 700;
  font-size: 2.5rem;
  color: #423125;
  margin-bottom: 20px;
}

.product-description {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem;
  line-height: 1.6;
  color: #423125;
  margin-bottom: 30px;
}

.product-price {
  font-family: 'Aclonica', sans-serif;
  font-size: 2rem;
  color: #423125;
  margin-bottom: 30px;
}

.buy-button {
  display: inline-block;
  padding: 15px 30px;
  background-color: #423125;
  color: white;
  text-decoration: none;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-size: 1.2rem;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  text-align: center;
}

.buy-button:hover {
  background-color: #5a4a3a;
}

@media (max-width: 768px) {
  .bag-detail-container {
    flex-direction: column;
    padding: 20px;
  }
  
  .image-container {
    width: 100%;
    height: 50vh;
  }
  
  .product-info {
    padding: 20px;
  }
  
  .product-title {
    font-size: 2rem;
  }
  
  .product-description {
    font-size: 1.2rem;
  }
}
</style>