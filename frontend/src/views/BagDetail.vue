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
      <div class="content-wrapper">
        <!-- Image Section -->
        <div class="image-section">
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

          <div class="image-container" ref="imageContainer"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd">
            <div class="image-track" :style="{ transform: `translateX(${imageTrackOffset}px)` }">
              <div v-for="(image, index) in images" :key="index" class="image-wrapper">
                <img
                  :src="image.preview || image.url"
                  :alt="bag.name"
                  class="bag-image"
                />
                <button class="edit-image-button" @click="openCropModal(index)">
                  <i class="fas fa-edit"></i>
                </button>
              </div>
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

            <transition name="fade-slide" mode="out-in">
              <div class="editable-field" v-if="!editingDescription" key="description-view">
                <p class="section-text">{{ bag.description || 'Здесь будет находиться информация о сумке' }}</p>
                <span class="edit-icon" @click="editDescription">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </span>
              </div>
              <div class="editable-field" v-else key="description-edit">
                <textarea v-model="descriptionInput" class="edit-input"></textarea>
                <div class="edit-buttons">
                  <button class="confirm-button" @click="saveDescription"><i data-v-d4900a64="" class="fas fa-check" style="scale: 77%;"></i></button>
                  <button class="cancel-button" @click="cancelEditDescription"><i data-v-d4900a64="" class="fas fa-times" style="scale: 77%;"></i></button>
                </div>
              </div>
            </transition>

            <div class="price-section">
              <transition name="fade-slide" mode="out-in">
                <div class="price-container" v-if="!editingPrice" key="price-view">
                  <div class="price">{{ bag.price }}₽</div>
                  <span class="edit-icon" @click="editPrice">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </span>
                </div>
                <div class="price-container" v-else key="price-edit">
                  <input type="number" v-model.number="priceInput" class="edit-input" />
                  <div class="edit-buttons">
                    <button class="confirm-button" @click="savePrice"><i data-v-d4900a64="" class="fas fa-check" style="scale: 77%;"></i></button>
                    <button class="cancel-button" @click="cancelEditPrice"><i data-v-d4900a64="" class="fas fa-times" style="scale: 77%;"></i></button>
                  </div>
                </div>
              </transition>
              <a href="https://t.me/kurorooooo" class="buy-button" target="_blank">
                <span class="button-text">КУПИТЬ</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" class="telegram-icon">
                  <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Crop Modal -->
    <transition name="fade">
      <div v-if="showCropModal" class="crop-modal-overlay" :style="{ backgroundColor: cropModalBackground }">
        <div class="crop-modal-content">
          <div class="fixed-crop-container">
            <vue-cropper
              ref="cropper"
              :src="imageToCrop"
              :aspect-ratio="1/1.25751633987"
              :view-mode="1"
              :auto-crop-area="0.8"
              :zoomable="true"
              :movable="true"
              :scalable="true"
              :zoom-on-touch="true"
              :zoom-on-wheel="true"
              :drag-mode="'move'"
              :min-container-width="700"
              :min-container-height="500"
              :min-canvas-width="200"
              :min-canvas-height="200"
              :crop-box-movable="true"
              :crop-box-resizable="true"
              :toggle-drag-mode-on-dblclick="false"
              guides
              background-class="cropper-background"
              @ready="onCropperReady"
            ></vue-cropper>
          </div>
          <div class="crop-controls">
            <button @click="cancelCrop" class="crop-button cancel">
              <i class="fas fa-times"></i>
            </button>
            <button @click="applyCrop" class="crop-button confirm">
              <i class="fas fa-check"></i>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Add Images Modal -->
    <transition name="fade">
      <div v-if="showAddImagesModal" class="modal-overlay">
        <div class="modal-content">
          <h3 class="error-title">Добавить изображения</h3>
          <div class="file-upload-group">
            <label for="new-images" class="file-upload-label">
              <span class="file-upload-text">
                {{ newImages.length > 0 ? `Выбрано ${newImages.length} фото (осталось ${remainingImageSlots})` : `Загрузите фото (осталось ${remainingImageSlots})` }}
              </span>
              <span class="file-upload-button">Загрузить</span>
              <input 
                type="file" 
                id="new-images" 
                @change="handleNewFileUpload" 
                accept="image/*"
                class="file-upload-input"
                multiple
                :disabled="remainingImageSlots <= 0"
              >
            </label>
            <div v-if="remainingImageSlots <= 0" class="upload-limit-reached">
              Достигнут лимит в 10 изображений
            </div>
          </div>
          
          <div class="image-preview-container">
            <draggable 
              v-model="newImages" 
              tag="div" 
              class="image-preview-list" 
              item-key="id"
              handle=".preview-image"
            >
              <template #item="{element, index}">
                <div class="image-preview-item">
                  <img 
                    :src="element.preview" 
                    class="preview-image" 
                    @click="openCropModalForNewImage(index)"
                  />
                  <button @click="removeNewImage(index)" class="remove-image-button">
                    <i class="fas fa-times"></i>
                  </button>
                  <div v-if="!element.isNew" class="existing-image-tag">Existing</div>
                  <!-- <div class="drag-handle">
                    <i class="fas fa-arrows-alt"></i>
                  </div> -->
                </div>
              </template>
            </draggable>
          </div>
          
          <div class="modal-buttons">
            <button @click="saveNewImages" class="modal-button confirm">Сохранить</button>
            <button @click="cancelAddImages" class="modal-button cancel">Отмена</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Edit Images Button -->
    <button v-if="!loading" class="edit-images-button" @click="openAddImagesModal">
      <i class="fas fa-plus"></i> Загрузить изображения
    </button>
  </div>
</template>

<script>
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import draggable from 'vuedraggable';

export default {
  name: 'BagDetail',
  components: {
    VueCropper,
    draggable
  },
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      bag: {},
      images: [], // Array of image objects with preview and file data
      currentImageIndex: 0,
      loading: true,
      imageTrackOffset: 0,
      imageWidth: 0,
      // Editing states
      editingDescription: false,
      editingPrice: false,
      // For Editing
      descriptionInput: '',
      priceInput: '',
      // Image editing
      showCropModal: false,
      imageToCrop: '',
      currentEditingIndex: 0,
      // New images
      showAddImagesModal: false,
      newImages: [],
      isEditingNewImage: false,
      cropModalBackground: 'rgba(0, 0, 0, 0.8)', // default
      touchStartX: 0,
      touchEndX: 0,
      isSwiping: false,
      touchStartTime: 0,
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
    },
    'bag.description': {
      handler(newVal) {
        this.descriptionInput = newVal;
      },
      immediate: true
    },
    'bag.price': {
      handler(newVal) {
        this.priceInput = newVal;
      },
      immediate: true
    }
  },
  methods: {
    handleTouchStart(e) {
      if (this.images.length <= 1) return;
      this.touchStartX = e.touches[0].clientX;
      this.touchStartTime = Date.now();
      this.isSwiping = true;
      
      // Disable transitions during swipe
      const imageTrack = this.$refs.imageContainer.querySelector('.image-track');
      imageTrack.style.transition = 'none';
    },
    
    handleTouchMove(e) {
      if (!this.isSwiping || this.images.length <= 1) return;
      e.preventDefault();
      
      this.touchEndX = e.touches[0].clientX;
      const diff = this.touchStartX - this.touchEndX;
      
      // Calculate potential new offset
      let newOffset = -this.currentImageIndex * this.imageWidth - diff;
      
      // Apply boundaries with rubber band effect
      const maxOffset = 0;
      const minOffset = -(this.images.length - 1) * this.imageWidth;
      
      if (newOffset > maxOffset) {
        // Apply rubber band effect at start
        newOffset = maxOffset + (newOffset - maxOffset) * 0.3;
      } else if (newOffset < minOffset) {
        // Apply rubber band effect at end
        newOffset = minOffset + (newOffset - minOffset) * 0.3;
      }
      
      const imageTrack = this.$refs.imageContainer.querySelector('.image-track');
      imageTrack.style.transition = 'none';
      imageTrack.style.transform = `translateX(${newOffset}px)`;
    },
    
    handleTouchEnd() {
      if (!this.isSwiping || this.images.length <= 1) return;
      this.isSwiping = false;
      
      const threshold = this.imageWidth * 0; // 15% of image width as threshold
      const diff = this.touchStartX - this.touchEndX;
      const velocity = Math.abs(diff) / (Date.now() - this.touchStartTime);
      
      const imageTrack = this.$refs.imageContainer.querySelector('.image-track');
      imageTrack.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
      
      // Check if swipe was fast enough or moved far enough
      if ((Math.abs(diff) > threshold || velocity > 0.3)) {
        if (diff > 0 && this.currentImageIndex < this.images.length - 1) {
          // Swipe left - go to next image
          this.setCurrentImageIndex(this.currentImageIndex + 1);
        } else if (diff < 0 && this.currentImageIndex > 0) {
          // Swipe right - go to previous image
          this.setCurrentImageIndex(this.currentImageIndex - 1);
        } else {
          // Return to current image if at boundary
          this.scrollToImage();
        }
      } else {
        // Not enough swipe - spring back to current position
        this.scrollToImage();
      }
    },
    
    handleSwipe() {
      if (this.images.length <= 1) return;
      
      const threshold = 50; // minimum swipe distance to trigger
      const diff = this.touchStartX - this.touchEndX;
      
      if (diff > threshold) {
        // Swipe left - go to next image
        this.nextImage();
      } else if (diff < -threshold) {
        // Swipe right - go to previous image
        this.prevImage();
      }
    },
    checkImageSize() {
      if (this.$refs.cropper) {
        const canvasData = this.$refs.cropper.getCanvasData();
        const cropBoxData = this.$refs.cropper.getCropBoxData();
        
        // Check if image is smaller than crop box in either dimension
        if (canvasData.width < cropBoxData.width || canvasData.height < cropBoxData.height) {
          // Calculate the minimum scale needed to fit the crop box
          const minScale = Math.max(
            cropBoxData.width / canvasData.naturalWidth,
            cropBoxData.height / canvasData.naturalHeight
          );
          
          // Set the minimum canvas dimensions to match crop box
          this.$refs.cropper.setCanvasData({
            width: cropBoxData.width,
            height: cropBoxData.height
          });
          
          // Reset zoom to minimum scale
          this.$refs.cropper.zoomTo(minScale);
          return false;
        }
      }
      return true;
    },
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
        // Convert existing images to our format
        this.images = data.images.map(img => ({
          url: img.url,
          preview: img.url,
          id: img.id, // Keep the original ID for existing images
          isNew: false
        }));
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
      this.$nextTick(() => {
        this.calculateImageWidth();
        const imageTrack = this.$refs.imageContainer.querySelector('.image-track');
        if (imageTrack) {
          imageTrack.style.transition = 'transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
          this.imageTrackOffset = -this.currentImageIndex * this.imageWidth;
        }
      });
    },
    //Edit Functions
    editDescription() {
      this.editingDescription = true;
      this.descriptionInput = this.bag.description || '';
    },
    editPrice() {
      this.editingPrice = true;
      this.priceInput = this.bag.price || '';
    },
    async saveDescription() {
      try {
        const response = await fetch(`/api/bags/${this.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            description: this.descriptionInput
          })
        });

        if (!response.ok) {
          throw new Error('Failed to save description');
        }

        this.bag.description = this.descriptionInput;
        this.editingDescription = false;
      } catch (error) {
        console.error('Error saving description:', error);
        alert('Failed to save description');
      }
    },
    async savePrice() {
      try {
        const response = await fetch(`/api/bags/${this.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            price: this.priceInput
          })
        });

        if (!response.ok) {
          throw new Error('Failed to save price');
        }

        this.bag.price = this.priceInput;
        this.editingPrice = false;
      } catch (error) {
        console.error('Error saving price:', error);
        alert('Failed to save price');
      }
    },
    cancelEditDescription() {
      this.editingDescription = false;
      this.descriptionInput = this.bag.description;
    },
    cancelEditPrice() {
      this.editingPrice = false;
      this.priceInput = this.bag.price;
    },
    // Image editing methods
    openCropModal(index) {
      this.currentEditingIndex = index;
      this.imageToCrop = this.images[index].preview;
      this.isEditingNewImage = false;
      this.showCropModal = true;
      
      this.$nextTick(() => {
        if (this.$refs.cropper) {
          const container = this.$refs.cropper.$el;
          const isMobile = window.innerWidth < 1000;
      
          if (isMobile) {
            container.style.width = '';
            container.style.height = 'calc(100vh - 100px)';
          } else {
            container.style.width = '700px';
            container.style.height = '500px';
          }
          container.style.overflow = 'hidden';
          this.$refs.cropper.replace(this.imageToCrop);
          this.$refs.cropper.reset();
          this.$refs.cropper.setAspectRatio(1/1.25751633987);
          this.$refs.cropper.setDragMode('move');
          
          // Get dimensions after initialization
          const cropBoxData = this.$refs.cropper.getCropBoxData();
          const containerData = this.$refs.cropper.getContainerData();
          
          // Set minimum dimensions
          this.$refs.cropper.setCanvasData({
            minWidth: cropBoxData.width,
            minHeight: cropBoxData.height
          });
          
          this.$refs.cropper.setCropBoxData({
            minWidth: cropBoxData.width,
            minHeight: cropBoxData.height,
            maxWidth: containerData.width,
            maxHeight: containerData.height
          });
          
          // Limit crop box movement
          this.$refs.cropper.setData({
            minLeft: 0,
            minTop: 0,
            maxLeft: containerData.width - cropBoxData.width,
            maxTop: containerData.height - cropBoxData.height
          });
          // Add event listeners
          this.$refs.cropper.$el.addEventListener('wheel', this.handleCropperWheel);
          this.$refs.cropper.$el.addEventListener('touchmove', this.handleCropperTouch);
          
          // Initial check
          this.checkImageSize();
        }
      });
    },
    onCropperReady() {
      if (this.$refs.cropper) {
        // Set initial zoom to fit the image within the container
        this.$refs.cropper.zoomTo(0.5);
        
        // Get crop box dimensions
        const cropBoxData = this.$refs.cropper.getCropBoxData();
        const containerData = this.$refs.cropper.getContainerData();
        
        // Set minimum dimensions for the canvas (image) to match crop box size
        this.$refs.cropper.setCanvasData({
          minWidth: cropBoxData.width,
          minHeight: cropBoxData.height
        });
        
        // Also set minimum dimensions for the crop box itself
        this.$refs.cropper.setCropBoxData({
          minWidth: cropBoxData.width,
          minHeight: cropBoxData.height,
          maxWidth: containerData.width,
          maxHeight: containerData.height
        });
        
        // Limit the movement of the crop box
        this.$refs.cropper.setData({
          minLeft: 0,
          minTop: 0,
          maxLeft: containerData.width - cropBoxData.width,
          maxTop: containerData.height - cropBoxData.height
        });
        
        // Add event listeners to prevent making image smaller than crop box
        this.$refs.cropper.$el.addEventListener('wheel', this.handleCropperWheel);
        this.$refs.cropper.$el.addEventListener('touchmove', this.handleCropperTouch);
      }
    },
    handleCropperWheel(e) {
      if (!this.checkImageSize()) {
        e.preventDefault();
      }
    },
    
    handleCropperTouch(e) {
      if (!this.checkImageSize()) {
        e.preventDefault();
      }
    },
    cancelCrop() {
      this.cropModalBackground = 'rgba(0, 0, 0, 0.8)';
      this.showCropModal = false;
      this.imageToCrop = '';
    },
    applyCrop() {
      this.$refs.cropper.getCroppedCanvas().toBlob((blob) => {
        const fileName = 'cropped_' + Date.now() + '.png';
        const croppedFile = new File([blob], fileName, { type: 'image/png' });
        
        if (this.isEditingNewImage) {
          // For existing images in the upload modal, we need to mark them as modified
          const isExistingImage = !this.newImages[this.currentEditingIndex].isNew;
          
          if (isExistingImage) {
            // For existing images, we'll treat them as new uploads with the cropped version
            this.newImages[this.currentEditingIndex] = {
              ...this.newImages[this.currentEditingIndex],
              preview: URL.createObjectURL(blob),
              cropped: croppedFile,
              isNew: true // Mark as new to force upload
            };
          } else {
            // For truly new images
            this.newImages[this.currentEditingIndex].preview = URL.createObjectURL(blob);
            this.newImages[this.currentEditingIndex].cropped = croppedFile;
          }
        } else {
          // For main view cropping
          this.images[this.currentEditingIndex].preview = URL.createObjectURL(blob);
          this.images[this.currentEditingIndex].cropped = croppedFile;
        }
        
        this.cropModalBackground = 'rgba(0, 0, 0, 0.8)';

        this.showCropModal = false;
      }, 'image/png');
    },
    // New images methods
    openAddImagesModal() {
      this.showAddImagesModal = true;
      // Initialize with existing images marked as not new
      this.newImages = this.images.map(img => ({
        ...img,
        isNew: false
      }));
    },
    handleNewFileUpload(event) {
      const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
      const MAX_TOTAL_IMAGES = 10;
      const files = event.target.files;
      
      if (!files || files.length === 0) return;

      // Filter out any null or undefined files
      const validFiles = Array.from(files).filter(file => file);
      
      // Calculate available slots considering existing newImages
      const availableSlots = MAX_TOTAL_IMAGES - this.newImages.length;
      
      if (validFiles.length > availableSlots) {
        alert(`Вы можете добавить максимум ${availableSlots} изображений (всего не более ${MAX_TOTAL_IMAGES})`);
        event.target.value = '';
        return;
      }

      // Process each valid file
      validFiles.slice(0, availableSlots).forEach((file) => {
        if (file.size > MAX_FILE_SIZE) {
          alert('Размер изображения должен быть меньше 5MB');
          return;
        }
        
        if (file && file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.newImages.push({
              file: file,
              preview: e.target.result,
              cropped: null,
              isNew: true
            });
          };
          reader.readAsDataURL(file);
        }
      });
      
      event.target.value = '';
    },
    openCropModalForNewImage(index) {
      this.currentEditingIndex = index;
      const image = this.newImages[index];
      
      // If it's an existing image, use its URL directly
      if (!image.isNew) {
        this.imageToCrop = image.url;
      } else {
        // For new images, use the preview
        this.imageToCrop = image.preview;
      }
      
      this.isEditingNewImage = true;
      this.showCropModal = true;

      this.cropModalBackground = 'rgba(0, 0, 0, 0.1)';
      
      this.$nextTick(() => {
        if (this.$refs.cropper) {
          const container = this.$refs.cropper.$el;
          const isMobile = window.innerWidth < 1000;
      
          if (isMobile) {
            container.style.width = '';
            container.style.height = 'calc(100vh - 100px)';
          } else {
            container.style.width = '700px';
            container.style.height = '500px';
          }
          container.style.overflow = 'hidden';
          this.$refs.cropper.replace(this.imageToCrop);
          this.$refs.cropper.reset();
          this.$refs.cropper.setAspectRatio(1/1.25751633987);
          this.$refs.cropper.setDragMode('move');
          
          // Get dimensions after initialization
          const cropBoxData = this.$refs.cropper.getCropBoxData();
          const containerData = this.$refs.cropper.getContainerData();
          
          // Set minimum dimensions
          this.$refs.cropper.setCanvasData({
            minWidth: cropBoxData.width,
            minHeight: cropBoxData.height
          });
          
          this.$refs.cropper.setCropBoxData({
            minWidth: cropBoxData.width,
            minHeight: cropBoxData.height,
            maxWidth: containerData.width,
            maxHeight: containerData.height
          });
          
          // Limit crop box movement
          this.$refs.cropper.setData({
            minLeft: 0,
            minTop: 0,
            maxLeft: containerData.width - cropBoxData.width,
            maxTop: containerData.height - cropBoxData.height
          });
          // Add event listeners
          this.$refs.cropper.$el.addEventListener('wheel', this.handleCropperWheel);
          this.$refs.cropper.$el.addEventListener('touchmove', this.handleCropperTouch);
          
          // Initial check
          this.checkImageSize();
        }
      });
    },
    removeNewImage(index) {
      // if (!this.newImages[index].isNew && !confirm('Удалить это изображение?')) {
      //   return;
      // }
      this.newImages.splice(index, 1);
    },
    cancelAddImages() {
      this.showAddImagesModal = false;
      this.newImages = [];
    },
    async saveNewImages() {
      try {
        const formData = new FormData();
        const newImagesToUpload = this.newImages.filter(img => img.isNew);
        
        if (newImagesToUpload.length > 0) {
          formData.delete('images[]');
          newImagesToUpload.forEach((image, index) => {
            const fileToUpload = image.cropped || image.file;
            formData.append('images[]', fileToUpload, fileToUpload.name);
          });
          
          const uploadResponse = await fetch(`/api/bags/${this.id}/images`, {
            method: 'POST',
            body: formData,
          });
          
          if (!uploadResponse.ok) {
            const errorData = await uploadResponse.json().catch(() => ({}));
            throw new Error(errorData.error || 'Failed to upload images');
          }
          
          const result = await uploadResponse.json();
          console.log('Upload successful:', result);
          
          if (result.image_ids && result.image_ids.length > 0) {
            let uploadedIndex = 0;
            this.newImages.forEach((img, index) => {
              if (img.isNew) {
                img.id = result.image_ids[uploadedIndex];
                uploadedIndex++;
              }
            });
          }
        }

        // Create image order mapping for ALL images (including existing ones that weren't deleted)
        const imageOrder = {};
        this.newImages.forEach((image, index) => {
          if (image.id) {
            imageOrder[image.id] = index;
          }
        });

        // If no images left, send empty order to delete all images
        const orderResponse = await fetch(`/api/bags/${this.id}/images/order`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ order: imageOrder })
        });

        if (!orderResponse.ok) {
          const errorData = await orderResponse.json().catch(() => ({}));
          throw new Error(errorData.error || 'Failed to update image order');
        }
        
        // Force refresh the bag details instead of just fetching
        this.loading = true;
        await this.fetchBagDetails();
        
        this.showAddImagesModal = false;
        this.newImages = [];
        
      } catch (error) {
        console.error('Error saving images:', error);
        alert(`Ошибка при сохранении: ${error.message}`);
      }
    },
    async deleteImage(imageId) {
      // if (!confirm('Удалить это изображение?')) {
      //   return;
      // }
      
      try {
        const response = await fetch(`/api/bags/${this.id}/images/${imageId}`, {
          method: 'DELETE'
        });
        
        if (!response.ok) {
          throw new Error('Failed to delete image');
        }
        
        // Refresh the bag details
        await this.fetchBagDetails();
      } catch (error) {
        console.error('Error deleting image:', error);
        alert('Произошла ошибка при удалении изображения');
      }
    }
  },
  mounted() {
    this.fetchBagDetails();
    
    if (this.$refs.imageContainer) {
      this.$refs.imageContainer.addEventListener('touchstart', this.handleTouchStart, { passive: false });
      this.$refs.imageContainer.addEventListener('touchmove', this.handleTouchMove, { passive: false });
      this.$refs.imageContainer.addEventListener('touchend', this.handleTouchEnd, { passive: true });
    }
  },
  beforeDestroy() {
    if (this.$refs.cropper) {
      this.$refs.cropper.$el.removeEventListener('wheel', this.handleCropperWheel);
      this.$refs.cropper.$el.removeEventListener('touchmove', this.handleCropperTouch);
    }
    
    if (this.$refs.imageContainer) {
      this.$refs.imageContainer.removeEventListener('touchstart', this.handleTouchStart);
      this.$refs.imageContainer.removeEventListener('touchmove', this.handleTouchMove);
      this.$refs.imageContainer.removeEventListener('touchend', this.handleTouchEnd);
    }
  },
  computed: {
    remainingImageSlots() {
      const MAX_TOTAL_IMAGES = 10;
      return MAX_TOTAL_IMAGES - this.newImages.length;
    }
  }
}
</script>

<style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.3s ease;
  }

  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }

  /* For the modal content, we'll add a separate transition */
  .modal-content-enter-active,
  .modal-content-leave-active {
    transition: all 0.3s ease;
  }

  .modal-content-enter-from,
  .modal-content-leave-to {
    opacity: 0;
    transform: translateY(20px);
  }
  .crop-modal-overlay,
  .modal-overlay {
    transition: opacity 0.3s ease;
  }
  .crop-modal-content,
  .modal-content {
    transition: all 0.3s ease;
  }
  .drag-handle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 30px;
    height: 30px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.2s;
    pointer-events: none;
  }

  .drag-handle i {
    color: white;
    font-size: 14px;
  }

  .image-preview-item:hover .drag-handle {
    opacity: 1;
  }

  /* Add this to make dragging more visible */
  .draggable-item-dragging {
    opacity: 0.8;
    transform: scale(1.05);
    z-index: 10;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  }

  .draggable-ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }
  .upload-limit-reached {
    color: #ff6b6b;
    margin-top: 8px;
    font-size: 0.9rem;
    text-align: center;
  }

  .file-upload-input:disabled + .file-upload-label {
    opacity: 0.5;
    pointer-events: none;
  }
  .file-upload-input:disabled + .file-upload-label {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .file-upload-input:disabled + .file-upload-label .file-upload-button {
    background-color: #cccccc;
  }
  .existing-image-tag {
    position: absolute;
    bottom: 3px;
    left: 3px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 10px;
  }
  /* Add these new styles for image editing */
  .image-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    flex-shrink: 0;
  }

  .edit-image-button {
    position: absolute;
    bottom: 15px;
    right: 15px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 10;
  }

  .edit-image-button:hover {
    background-color: rgba(0, 0, 0, 0.8);
    transform: scale(1.1);
  }

  .edit-image-button i {
    font-size: 16px;
  }

  .edit-images-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 15px;
    background-color: #423125;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-size: 1rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
  }

  .edit-images-button:hover {
    background-color: #2a1f18;
    transform: translateY(-2px);
  }

  /* Crop Modal Styles (same as in AddItem.vue) */
  .crop-modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1001;
  }

  .crop-modal-content {
    border-radius: 12px;
    display: flex;
    flex-direction: column;
  }

  .fixed-crop-container {
    position: relative;
    background-color: #f4ebe2;
    width: 700px;
    height: 500px;
    overflow: hidden; /* Add this to prevent content from expanding the container */
    margin: 0 auto; /* Center the container */
  }

  .cropper-container {
    width: 100% !important;
    height: 100% !important;
    position: absolute;
    top: 0;
    left: 0;
    overflow: hidden !important;
  }

  .cropper-crop-box, 
  .cropper-view-box, 
  .cropper-canvas {
    width: 100% !important;
    height: 100% !important;
  }
  
  .cropper-wrap-box {
    overflow: hidden !important;
    width: 700px !important;
    height: 500px !important;
  }

  .cropper-background {
    width: 700px !important;
    height: 500px !important;
    max-width: 700px !important;
    max-height: 500px !important;
  }

  .cropper-container cropper-bg {
    width: 700px !important;
    height: 500px !important;
    max-width: 700px !important;
    max-height: 500px !important;
  }

  .crop-controls {
    display: flex;
    justify-content: space-between;
    bottom: 20px;
    left: 0;
    right: 0;
    padding: 0 20px;
    padding-top: 15px;
    z-index: 10;
  }

  .crop-button {
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

  .crop-button:hover {
    background-color: rgba(0, 0, 0, 0.8);
    transform: scale(1.1);
  }

  .crop-button i {
    color: rgba(255, 255, 255, 0.9);
  }

  .crop-button.cancel:hover i {
    color: #ff6b6b;
  }

  .crop-button.confirm:hover i {
    color: #51cf66;
  }

  /* Add Images Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    background-color: #f4ebe2;
    padding: 30px;
    border-radius: 12px;
    max-width: 521px;
    width: 90%;
    text-align: center;
    border: 1px solid #d0cbc4;
  }

  .error-title {
    color: #423125;
    font-weight: 700;
    margin-bottom: 17px;
    margin-top: 0;
    font-size: 1.7rem;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
  }

  .modal-buttons {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
  }

  .modal-button {
    padding: 8px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-weight: 600;
  }

  .modal-button.confirm {
    background-color: #423125;
    color: white;
  }

  .modal-button.confirm:hover {
    background-color: #2a1f18;
  }

  .modal-button.cancel {
    background-color: #d0cbc4;
    color: #423125;
  }

  .modal-button.cancel:hover {
    background-color: #c5beb6;
  }

  /* Image preview styles (same as in AddItem.vue) */
  .image-preview-container {
    margin-top: 15px;
  }

  .image-preview-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
    border: dotted;
    border-color: rgb(208 203 196);
    border-radius: 10px;
    padding: 5px;
    justify-content: center;
  }

  .image-preview-item {
    position: relative;
    width: 80px;
    height: 80px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
    cursor: move;
  }

  .image-preview-item:hover {
    transform: scale(1.05);
  }

  .preview-image {
    cursor: pointer;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.2s;
  }

  .preview-image:hover {
    transform: scale(1.05);
  }

  .remove-image-button {
    position: absolute;
    top: 3px;
    right: 3px;
    width: 17px;
    height: 16px;
    border-radius: 50%;
    background-color: rgba(255, 0, 0, 0.7);
    color: white;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 10px;
    padding: 0;
  }

  /* File upload styles (same as in AddItem.vue) */
  .file-upload-group {
    margin-bottom: 20px;
  }

  .file-upload-label {
    display: flex;
    cursor: pointer;
  }

  .file-upload-text {
    flex-grow: 1;
    padding: 12px;
    border: 1px solid #d0cbc4;
    border-radius: 8px 0 0 8px;
    background-color: rgba(255, 255, 255, 0.8);
    color: #423125;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-weight: 600;
  }

  .file-upload-button {
    padding: 12px 15px;
    background-color: #d0cbc4;
    color: #423125;
    border: 1px solid #d0cbc4;
    border-radius: 0 8px 8px 0;
    font-size: 0.9rem;
    transition: background-color 0.3s ease;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-weight: 600;
  }

  .file-upload-button:hover {
    background-color: #c5beb6;
  }

  .file-upload-input {
    display: none;
  }

  @media (max-width: 1000px) {
    .fixed-crop-container {
      width: 90vw;
      height: 90vw;
      max-width: 400px;
      max-height: 400px;
    }

    .edit-images-button {
      bottom: 10px;
      right: 10px;
      font-size: 0.9rem;
      padding: 8px 12px;
    }
  }

  /* Keep all existing styles from the original file */
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700;900&family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

  .bag-detail-page {
    display: flex;
    height: 100vh;
    overflow: hidden;
    position: relative;
  }

  .content-wrapper {
    display: flex;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  .disabled {
    opacity: 0.3;
    pointer-events: none;
    cursor: not-allowed;
  }

  /* Loading overlay styles */
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(244, 235, 226, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10;
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
    width: calc(100vh / 1.25751633987); /* Calculate width based on viewport height */
    height: 100vh;
    position: relative;
    background-color: #f4ebe2;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0; /* Prevent shrinking */
  }

  .image-container {
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  .image-container {
    -webkit-overflow-scrolling: touch;
    touch-action: pan-y;
  }

  .image-track {
    display: flex;
    flex-direction: row;
    height: 100%;
    transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    will-change: transform; /* Optimize for performance */
  }
  
  .image-track.no-transition {
    /* transition: none !important; */
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
    flex-shrink: 0;
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
    flex-grow: 1;
    overflow-y: auto;
    padding: 40px;
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
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-weight: 700;
    font-size: 1.8rem;
    line-height: 1.3;
    color: #423125;
    letter-spacing: 0.2px;
    margin: 0;
    margin-bottom: 10px;
  }

  .price-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 40px;
  }

  .price-container {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
  }

  .price-container input.edit-input {
    font-family: 'Aclonica', sans-serif;
    font-size: 2.5rem;
    color: #423125;
    padding: 0;
    width: auto;
    max-width: 200px;
  }

  textarea.edit-input {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 700;
    font-size: 1.8rem;
    line-height: 1.3;
    color: #423125;
    /* min-height: 120px; */
    resize: vertical;
    background-color: rgba(255, 255, 255, 0.3);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 4px;
    padding: 10px;
  }

  .price {
    font-family: 'Aclonica', sans-serif;
    font-size: 2.5rem;
    color: #333333;
    transition: all 0.3s ease;
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
    /* margin-left: 8px; */
    font-size: 1.2em;
    color: #777;
    /* Adjust color as needed */
    transition: color 0.2s;
  }

  .edit-icon:hover {
    color: #333;
  }

  .editable-field {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    transition: all 0.3s ease;
  }

  .edit-input {
    padding: 8px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-right: 8px;
    width: 100%;
    box-sizing: border-box; /* Ensures padding doesn't affect width */
    background-color: #ffffff80;
    transition: all 0.3s ease;
    overflow: hidden;
  }

  .edit-buttons {
    display: flex;
    gap: 5px;
    justify-content: space-between;
    /* padding: 0px 10px; */
    padding-top: 5px;
    padding-left: 5px;
    transition: all 0.3s ease;
  }

  .edit-buttons button {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: none;
    background-color: rgba(0, 0, 0, 0);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1.5rem;
    backdrop-filter: blur(5px);
    padding: 0;
  }

  /* Animation for edit sections */
  .editable-field-enter-active,
  .editable-field-leave-active {
    transition: all 0.3s ease;
  }

  .editable-field-enter-from,
  .editable-field-leave-to {
    opacity: 0;
    transform: translateY(10px);
  }

  /* Transition styles */
  .fade-slide-enter-active,
  .fade-slide-leave-active {
    transition: all 0.3s ease;
  }

  .fade-slide-enter-from {
    opacity: 0;
    transform: translateY(-10px);
  }

  .fade-slide-leave-to {
    opacity: 0;
    transform: translateY(10px);
  }
  
  .confirm-button:hover i {
    color: #51cf66;
    transform: scale(1.17);
    transition: all 0.3s ease;
  }
  
  .cancel-button:hover i {
    color: #ff6b6b;
    transform: scale(1.17);
    transition: all 0.3s ease;
  }
  
  .confirm-button i {
    transition: all 0.3s ease;
  }
  
  .cancel-button i {
    transition: all 0.3s ease;
  }

  @media (max-width: 1000px) {
    .bag-detail-page {
      flex-direction: column;
      height: auto;
      overflow-y: auto; /* Allow scrolling for the whole page */
    }

    .content-wrapper {
      flex-direction: column;
      height: auto;
    }

    .image-section {
      width: 100%;
      height: calc(100vw * 1.25751633987); /* Calculate height based on viewport width */
      min-height: 20vh;
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
      padding-bottom: 50px;
    }

    .text-content {
      min-width: 250px;
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
  @media (max-width: 1000px) {
    .fixed-crop-container {
      width: calc(100vw - 20px); /* Full width minus some padding */
      height: calc(100vh - 100px); /* Full height minus buttons space */
      max-width: none;
      max-height: none;
    }

    .cropper-background {
      width: 100% !important;
      height: 100% !important;
      max-width: 100% !important;
      max-height: 100% !important;
    }

    .cropper-wrap-box {
      overflow: hidden !important;
      width: 100% !important;
      height: 100% !important;
    }

    .cropper-container cropper-bg {
      width: 100% !important;
      height: 100% !important;
      max-width: 100% !important;
      max-height: 100% !important;
    }

    .crop-modal-content {
      width: 100%;
      height: 100%;
      justify-content: flex-start;
      padding-top: 20px;
    }

    .crop-controls {
      position: fixed;
      bottom: 20px;
      left: 0;
      right: 0;
      padding: 0 20px;
      justify-content: center;
      gap: 20px;
      z-index: 10;
    }

    .crop-button {
      width: 45px;
      height: 45px;
      position: relative;
    }
  }
  @media (max-width: 500px) {

    .price-section {
      flex-direction: column;
    }
  }
</style>