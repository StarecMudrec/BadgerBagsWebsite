<template>
  <div class="bag-detail-page">
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <p class="loading-text">Загрузка...</p>
      </div>
    </div>

    <!-- Content (shown when not loading) -->
    <template v-else>
      <!-- Image Section -->
      <div class="image-section" @wheel="handleWheel">
        <div class="arrow-nav left" @click="prevImage" :class="{ 'disabled': images.length <= 1 }">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="6 6 12 12" width="36" height="36">
            <defs>
              <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
                <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
              </filter>
            </defs>
            <path class="arrow-path" fill="white" filter="url(#arrowShadow)" d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/>
          </svg>
        </div>

        <div class="image-container">
          <div class="image-track" :style="{ transform: `translateX(${imageTrackOffset}px)` }">
            <img
              v-for="(image, index) in images"
              :key="index"
              :src="image"
              :alt="bag.name"
              class="bag-image"
            />
          </div>
        </div>

        <div class="arrow-nav right" @click="nextImage" :class="{ 'disabled': images.length <= 1 }">
          <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="6 6 12 12" width="36" height="36">
            <defs>
              <filter id="arrowShadow" x="-20%" y="-20%" width="140%" height="150%">
                <feDropShadow dx="0" dy="0.5" stdDeviation="0.5" flood-color="rgba(0,0,0,0.3)"/>
                <feDropShadow dx="0" dy="0" stdDeviation="0.2" flood-color="rgba(0,0,0,0.15)"/>
              </filter>
            </defs>
            <path class="arrow-path" fill="white" filter="url(#arrowShadow)" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </div>

        <!-- Image Dots -->
        <div class="image-dots">
          <span
            v-for="(image, index) in images"
            :key="index"
            class="image-dot"
            :class="{ 'active': index === currentImageIndex }"
            @click="setCurrentImageIndex(index)"
          ></span>
        </div>
      </div>

      <!-- Text Section (60% width) -->
      <div class="text-section">
        <div class="text-content">
          <h2 class="section-title">О сумке:</h2>
          <div class="editable-field">
            <p class="section-text">{{ bag.description || 'Здесь будет находиться информация о сумке' }}</p>
            <span class="edit-icon" @click="editDescription">✏️</span>
          </div>

          <div class="price-section">
            <div class="price-container">
                <div class="price">{{ bag.price }}₽</div>
                <span class="edit-icon" @click="editPrice">✏️</span>
            </div>
            <a href="https://t.me/kurorooooo" class="buy-button" target="_blank">
              <span class="button-text">КУПИТЬ</span>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" class="telegram-icon">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: 'BagDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      bag: {},
      images: [], // Array of image URLs
      currentImageIndex: 0,
      loading: true,
      imageTrackOffset: 0,
      imageWidth: 0,
      //Editing states
      editingDescription: false,
      editingPrice: false
    }
  },
  watch: {
    currentImageIndex() {
      this.scrollToImage();
    },
    images() {
      this.$nextTick(() => {
        this.calculateImageWidth();
        this.scrollToImage();
      });
    }
  },
  methods: {
    async fetchBagDetails() {
      this.loading = true;
      try {
        const response = await fetch(`/api/bags/${this.id}`);

        if (!response.ok) {
          const error = await response.json().catch(() => ({ error: 'Unknown error' }));
          throw new Error(error.message || 'Failed to fetch bag details');
        }

        const data = await response.json();
        this.bag = data;
        // Store all image URLs in the images array
        this.images = data.images.map(img => img.url);
      } catch (error) {
        console.error('Error fetching bag details:', error);
        if (error.message.includes('not found')) {
          this.$router.push('/not-found');
        }
      } finally {
        this.loading = false;
      }
    },
    nextImage() {
      if (this.images.length <= 1) return;
      this.setCurrentImageIndex((this.currentImageIndex + 1) % this.images.length);
    },
    prevImage() {
      if (this.images.length <= 1) return;
      this.setCurrentImageIndex((this.currentImageIndex - 1 + this.images.length) % this.images.length);
    },
    handleWheel(event) {
      if (this.images.length <= 1) return;
      //Reverse the wheel direction
      if (event.deltaY < 0) {
        this.nextImage();
      } else {
        this.prevImage();
      }
    },
    setCurrentImageIndex(index) {
      this.currentImageIndex = index;
    },
    calculateImageWidth() {
      const imageElement = document.querySelector('.bag-image');
      if (imageElement) {
        this.imageWidth = imageElement.clientWidth;
      }
    },
    scrollToImage() {
      //Use $nextTick to ensure DOM is updated
      this.$nextTick(() => {
        this.calculateImageWidth();
        this.imageTrackOffset = -this.currentImageIndex * this.imageWidth;
      });

    },
    //Edit Functions
    editDescription() {
      console.log("Edit Description Clicked"); //For testing
      //Here you would open a modal or replace the <p> tag with an <input> or <textarea>
      //and handle the saving of the updated description.
    },
    editPrice() {
      console.log("Edit Price Clicked"); //For testing
      //Similar to editDescription, you would open a modal or replace the <div> with an <input>
      //and handle the saving of the updated price.
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
    position: relative;
  }

  .disabled {
    opacity: 0.3;
    pointer-events: none;
    cursor: not-allowed;
  }

  /* Loading overlay styles */
  .loading-overlay {
    position: absolute;
    /* Changed from fixed to absolute */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(244, 235, 226, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
    /* Lower than navbar's z-index */
  }

  .loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 5px solid rgba(66, 49, 37, 0.2);
    border-radius: 50%;
    border-top-color: #423125;
    animation: spin 1s ease-in-out infinite;
  }

  .loading-text {
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-size: 2rem;
    color: #423125;
    font-weight: 700;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Rest of your existing styles remain the same */
  .image-section {
    width: 40%;
    min-width: 765px;
    height: 100vh;
    position: relative;
    background-color: #f4ebe2;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .image-container {
    width: 100%;
    height: 100%;
    overflow: hidden; /* Crucial for the scrolling effect */
  }

  .image-track {
    display: flex;
    flex-direction: row; /* Change to row for horizontal scrolling */
    /* width: max-content; Ensure the track is wide enough to hold all images */
    height: 100%; /* Ensure the track takes up the full height */
    transition: transform 0.27s ease-out; /* Smooth scrolling transition */
  }

  .bag-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
    min-width: 0;
    min-height: 0;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    flex-shrink: 0; /* Prevent images from shrinking */
  }

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

  /* Image dots styles */
  .image-dots {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 8px;
    z-index: 10;
  }

  .image-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.2);
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .image-dot.active {
    background-color: rgba(255, 255, 255, 0.7);
  }

  .text-section {
    width: 60%;
    padding: 40px 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
  }

  .text-content {
    width: 80%;
    max-width: 700px;
    min-width: 370px;
    align-self: center;
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

  .price-container{
    display: flex;
    align-items: center;
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
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  .buy-button:hover {
    background: rgba(255, 255, 255, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  }

  .buy-button:active {
    transform: translateY(0);
  }

  .buy-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0) 100%);
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

  /* Edit Icon Styles */
  .edit-icon {
    cursor: pointer;
    margin-left: 8px;
    font-size: 1.2em;
    color: #777; /* Adjust color as needed */
    transition: color 0.2s;
  }

  .edit-icon:hover {
    color: #333;
  }

  .editable-field{
    display: flex;
    align-items: center;
  }


  @media (max-width: 768px) {
    .bag-detail-page {
      flex-direction: column;
      height: auto;
    }

    .image-section {
      width: 100%;
      height: auto;
      min-height: 50vh;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 2px solid #ffffff;
    }

    .bag-image {
      width: 100%;
      height: auto;
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

    /*Image dots*/
    .image-dots {
      bottom: 10px;
      gap: 5px;
    }

    .image-dot {
      width: 8px;
      height: 8px;
    }
  }
</style>