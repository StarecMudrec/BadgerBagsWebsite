<template>
  <div class="add-item-page">
    <!-- Background image div -->
    <div class="background-image"></div>
    <!-- Error Modal -->
    <div v-if="showErrorModal" class="modal-overlay">
      <div class="modal-content">
        <h3 class="error-title">Error</h3>
        <p>{{ errorMessage }}</p>
        <button @click="closeModal" class="modal-button">OK</button>
      </div>
    </div>

    <!-- Crop Modal -->
    <div v-if="showCropModal" class="crop-modal-overlay">
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
            :min-container-width="200"
            :min-container-height="200"
            :min-canvas-width="200"
            :min-canvas-height="200"
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

    <div class="add-item-container">
      <h1>Добавьте товар</h1>
      <form @submit.prevent="submitForm" class="item-form">
        <div class="form-group">
          <label for="name">Название:</label>
          <input type="text" id="name" v-model="item.name" required>
        </div>
        
        <div class="form-group">
          <label for="description">Описание:</label>
          <textarea id="description" v-model="item.description" required></textarea>
        </div>
        
        <div class="form-group">
          <label for="price">Цена (₽):</label>
          <input type="number" id="price" v-model.number="item.price" required>
        </div>
        
        <div class="form-group">
          <label>Фотографии (до 10):</label>
          <div class="image-upload-container">
            <div class="file-upload-group" :class="{ 'has-error': fileError }">
              <label for="images" class="file-upload-label">
                <span class="file-upload-text">
                  {{ item.images.length > 0 ? `Выбрано ${item.images.length} фото` : 'Загрузите фото...' }}
                </span>
                <span class="file-upload-button">Загрузить</span>
                <input 
                  type="file" 
                  id="images" 
                  @change="handleFileUpload" 
                  accept="image/*"
                  class="file-upload-input"
                  multiple
                >
              </label>
              <span v-if="fileError" class="error-message">Пожалуйста, загрузите хотя бы одно фото</span>
            </div>
            
            <div class="image-preview-container">
              <draggable 
                v-model="item.images" 
                item-key="preview"
                @end="updateImageOrder"
                class="image-preview-list"
              >
                <template #item="{ element, index }">
                  <div class="image-preview-item">
                    <img 
                      :src="element.preview" 
                      class="preview-image" 
                      @click="openCropModal(index)"
                    />
                    <button @click="removeImage(index)" class="remove-image-button">
                      <i class="fas fa-times"></i>
                    </button>
                    <span class="image-position">{{ index + 1 }}</span>
                  </div>
                </template>
              </draggable>
            </div>
          </div>
          <div class="crop-instructions">
            <p>Вы можете обрезать изображения, нажав на их миниатюру выше</p>
            <!-- <p>You can crop images by clicking on their thumbnails above</p> -->
          </div>
        </div>
        
        <button 
          type="submit" 
          :disabled="isSubmitting || item.images.length === 0"
          class="submit-button"
        >
          <!-- <div class="spinner-container">
            <div class="spinner"></div>
          </div> -->
          <span v-if="!isSubmitting">Добавить</span>
          <div v-else class="spinner-container">
            <div class="spinner"></div>
          </div>
        </button>
      </form>
      
      <router-link to="/" class="back-link">← На главную</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';
import draggable from 'vuedraggable';

export default {
  name: 'AddItem',
  components: {
    VueCropper,
    draggable
  },
  data() {
    return {
      item: {
        name: '',
        description: '',
        price: null,
        images: []
      },
      showErrorModal: false,
      errorMessage: '',
      showCropModal: false,
      imageToCrop: '',
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      dragMode: 'none', // Initial drag mode
      isCropping: false,
      containerHeight: 'auto',
      dragMode: 'move', // Changed to 'move' to allow image movement
      fileError: false,
      isSubmitting: false,
      currentImageIndex: 0
    }
  },
  computed: {
    containerStyle() {
      return {
        height: this.containerHeight
      };
    }
  },
  methods: {
    openCropModal(index) {
      try {
        this.currentImageIndex = index;
        const image = this.item.images[index];
        
        if (!image || !image.preview) {
          throw new Error('No image available for cropping');
        }
        
        this.imageToCrop = image.preview;
        this.showCropModal = true;
        
        this.$nextTick(() => {
          if (this.$refs.cropper) {
            // First set the container dimensions
            const container = this.$refs.cropper.$el;
            container.style.width = '700px';
            container.style.height = '500px';
            
            // Then initialize the cropper
            this.$refs.cropper.replace(this.imageToCrop);
            this.$refs.cropper.reset();
            this.$refs.cropper.setAspectRatio(1/1.25751633987);
            this.$refs.cropper.setDragMode('move');
          }
        });
      } catch (error) {
        console.error('Error in crop modal:', error);
        this.showErrorModal = true;
        this.errorMessage = 'Failed to initialize image cropper.';
        this.showCropModal = false;
      }
    },
    handleFileUpload(event) {
      const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB limit
      const MAX_IMAGES = 10;
      const files = event.target.files;
      this.fileError = false;

      if (!files || files.length === 0) return;

      if (files.length + this.item.images.length > MAX_IMAGES) {
        this.errorMessage = `You can upload up to ${MAX_IMAGES} images`;
        this.showErrorModal = true;
        event.target.value = '';
        return;
      }

      // Process each file
      Array.from(files).forEach((file, index) => {
        if (file.size > MAX_FILE_SIZE) {
          this.errorMessage = 'Image size must be less than 5MB';
          this.showErrorModal = true;
          return;
        }
        
        if (file && file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              // Validate the image data
              if (!e.target.result.startsWith('data:image/')) {
                throw new Error('Invalid image format');
              }
              
              const newImage = {
                file: file,
                preview: e.target.result,
                cropped: null
              };
              this.item.images.push(newImage);
              
              // ... rest of your code
            } catch (error) {
              console.error('Error processing image:', error);
              this.showErrorModal = true;
              this.errorMessage = 'Failed to process image. Please try another one.';
            }
          };
          reader.onerror = () => {
            this.showErrorModal = true;
            this.errorMessage = 'Failed to read image file.';
          };
          reader.readAsDataURL(file);
        }
      });
      
      event.target.value = '';
    },
    removeImage(index) {
      this.item.images.splice(index, 1);
    },
    updateImageOrder() {
      // The order is automatically updated by draggable
    },
    async initializeCropper() {
      try {
        // Wait for cropper to be fully initialized
        await this.$nextTick();
        
        if (!this.$refs.cropper) return;
        
        // Set container dimensions
        const container = this.$refs.cropper.$el;
        container.style.width = '700px';
        container.style.height = '500px';
        container.style.overflow = 'hidden';
        
        // Reset and configure cropper
        this.$refs.cropper.reset();
        this.$refs.cropper.setAspectRatio(1/1.25751633987);
        this.$refs.cropper.setDragMode('move');
        
        // Wait for cropper to update
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Zoom to fit
        this.$refs.cropper.zoomTo(0.5);
        
      } catch (error) {
        console.error('Cropper initialization error:', error);
      }
    },
    onCropperReady() {
      try {
        // Set initial zoom to fit image nicely
        this.$refs.cropper.zoomTo(0.5);
        
        // Get the underlying cropper.js instance
        const cropperInstance = this.$refs.cropper.cropper;
        
        if (cropperInstance) {
          // Add zoom event listener the correct way
          cropperInstance.on('zoom', (event) => {
            const canvasData = cropperInstance.getCanvasData();
            const containerData = cropperInstance.getContainerData();
            
            // Prevent zooming in too far
            if (canvasData.width < containerData.width || 
                canvasData.height < containerData.height) {
              cropperInstance.zoomTo(1.0);
            }
          });
        }
      } catch (error) {
        console.error('Cropper ready handler:', error);
        // Don't show error modal since functionality still works
      }
    },

    onCropStart() {
      this.isCropping = true;
    },
    
    onCropEnd() {
      this.isCropping = false;
    },
    
    startDrag(e) {
      if (this.isCropping) return;
      
      this.isDragging = true;
      this.dragStartX = e.clientX;
      this.dragStartY = e.clientY;
      this.dragMode = 'none';
      e.preventDefault();
    },
    
    doDrag(e) {
      if (!this.isDragging || this.isCropping) return;
      
      const cropper = this.$refs.cropper;
      const moveX = e.clientX - this.dragStartX;
      const moveY = e.clientY - this.dragStartY;
      
      cropper.move(moveX, moveY);
      
      this.dragStartX = e.clientX;
      this.dragStartY = e.clientY;
    },
    
    endDrag() {
      this.isDragging = false;
      this.dragMode = 'crop'; // Reset to crop mode
    },
    cancelCrop() {
      this.showCropModal = false;
      this.imageToCrop = '';
    },
    applyCrop() {
      this.$refs.cropper.getCroppedCanvas().toBlob((blob) => {
        const fileName = 'cropped_' + Date.now() + '.png';
        const croppedFile = new File([blob], fileName, { type: 'image/png' });
        
        // Update the current image with cropped version
        this.item.images[this.currentImageIndex].cropped = croppedFile;
        this.item.images[this.currentImageIndex].preview = URL.createObjectURL(blob);
        
        this.showCropModal = false;
      }, 'image/png');
    },
    closeModal() {
      this.showErrorModal = false;
      this.errorMessage = '';
    },
    async submitForm() {
      if (this.isSubmitting) return;
      
      if (this.item.images.length === 0) {
        this.fileError = true;
        return;
      }

      this.isSubmitting = true;
      
      try {
        const formData = new FormData();
        formData.append('name', this.item.name);
        formData.append('description', this.item.description);
        formData.append('price', this.item.price);
        
        // Append all images
        this.item.images.forEach((image) => {
          formData.append('images[]', image.cropped || image.file);
        });

        const response = await axios.post('/api/bags', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          transformRequest: (data, headers) => {
            delete headers['Content-Type'];
            return data;
          },
          timeout: 30000 // 30 seconds timeout
        });
        
        if (response.data?.status === 'success') {
          this.$router.push('/');
        } else {
          throw new Error(response.data?.message || 'Invalid server response');
        }
      } catch (error) {
        let errorMsg = 'Ошибка при добавлении товара';
        
        if (error.code === 'ECONNABORTED') {
          errorMsg = 'Превышено время ожидания сервера';
        } else if (error.response) {
          if (typeof error.response.data === 'string' && 
              error.response.data.startsWith('<!DOCTYPE html>')) {
            errorMsg = 'Сервер вернул HTML вместо JSON';
          } else {
            errorMsg = error.response.data?.error || 
                      error.response.statusText || 
                      `HTTP ${error.response.status}`;
          }
        } else if (error.request) {
          errorMsg = 'Сервер не ответил';
        } else {
          errorMsg = error.message;
        }
        
        this.errorMessage = errorMsg;
        this.showErrorModal = true;
        console.error('Error details:', error);
      } finally {
        this.isSubmitting = false;
      }
    },  
    resetForm() {
      this.item = {
        name: '',
        description: '',
        price: null,
        image: null
      };
      const fileInput = document.getElementById('image');
      if (fileInput) {
        fileInput.value = '';
      }
    }
  }
}
</script>

<style scoped>           
  .spinner {
    width: 50px;
    height: 50px;
    border: 5px solid rgba(66, 49, 37, 0.2); /* Light brown with opacity */
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s ease-in-out infinite; /* Changed from linear to ease-in-out */
    margin: 0 auto;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .crop-instructions {
    margin-top: 10px;
    font-size: 0.9rem;
    color: #666;
    text-align: center;
    padding: 5px;
    background-color: #ffffff7d;
    border-radius: 4px;
  }

  .crop-instructions p {
    margin: 3px 0;
  }             
  .image-upload-container {
    margin-top: 10px;
  }

  .image-preview-container {
    margin-top: 15px;
  }

  .image-preview-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
    /* min-height: 50px;  */
    border: dotted;
    border-color: rgb(208 203 196);
    border-radius: 10px;
    padding: 5px;
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

  .image-preview-item.sortable-ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }

  .image-preview-item.sortable-chosen {
    opacity: 0.8;
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

  .image-position {
    position: absolute;
    bottom: 3px;
    left: 3px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 2px 6px;
    padding-top: 0;
    border-radius: 10px;
    font-size: 10px;
  }

  /* Make sure drag handles are visible */
  .image-preview-item {
    cursor: move;
    cursor: grab;
  }

  .image-preview-item:active {
    cursor: grabbing;
  }

  /* Add some visual feedback for dragging */
  .sortable-chosen {
    opacity: 0.8;
  }

  .sortable-ghost {
    opacity: 0.5;
    background: #c8ebfb;
  }

  .add-item-page {
    position: relative;
    min-height: 100vh;
    padding: 40px 20px;
    /* background: linear-gradient(to bottom, #f3efeb 0%, #e7e2dc 100%); */
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    --accent-color: #423125; /* Same as your current text color */
    --hover-color: #2a1f18; /* Darker shade for hover */
    --hover-border-color: #2a1f18; /* Color for underline */
  }

  /* Add these new styles for the background */
  .background-image {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('/background.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    filter: blur(8px) brightness(0.8);
    z-index: -1;
  }

  .add-item-container {
    max-width: 517px;
    margin: 0 auto;
    padding: 30px;
    background-color: #f3efebd9;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    margin-top: 100px;
    position: relative; /* Ensure it stays above the background */
  }

  h1 {
    text-align: center;
    color: #423125;
    font-size: 2.2rem;
    margin-top: 10px;
    font-weight: 700;
  }

  .item-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  label {
    font-size: 1rem;
    color: #423125;
    font-weight: 600;
  }

  input[type="text"],
  input[type="number"],
  textarea {
    padding: 12px;
    border: 1px solid #d0cbc4;
    border-radius: 8px;
    background-color: rgba(255, 255, 255, 0.8);
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    font-size: 1rem;
    transition: border-color 0.3s ease;
  }

  input[type="text"]:focus,
  input[type="number"]:focus,
  textarea:focus {
    outline: none;
    border-color: #a69d96;
  }

  textarea {
    min-height: 120px;
    resize: vertical;
  }

  /* File Upload Styles */
  .has-error .file-upload-label {
    border: 1px solid #ff4444;
    border-radius: 8px;
  }

  .error-message {
    color: #ff4444;
    font-size: 0.8rem;
    margin-top: 4px;
    display: block;
  }

  .file-upload-group {
    /* margin-bottom: 20px; */
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
    font-size: 1rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-upload-button {
    padding: 12px 15px;
    background-color: #d0cbc4;
    color: #423125;
    border: 1px solid #d0cbc4;
    border-radius: 0 8px 8px 0;
    font-size: 1rem;
    transition: background-color 0.3s ease;
  }

  .file-upload-button:hover {
    background-color: #c5beb6;
  }

  .file-upload-input {
    display: none;
  }

  .submit-button {
    width: 150px;
    position: relative;
    left: 50%;
    transform: translateX(-50%);
    padding: 14px;
    background-color: #423125;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    letter-spacing: 1px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 10px;
  }

  .submit-button:hover {
    background-color: #2a1f18;
  }

  .back-link {
    display: inline-block;
    margin-top: 20px;
    color: var(--accent-color);
    text-decoration: none;
    font-size: 1rem;
    transition: color 0.3s ease;
    position: relative;
    padding: 5px 0;
    font-family: 'Noto Serif TC', 'Noto Serif', serif;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
  }

  .back-link:hover {
    color: var(--hover-color);
    -webkit-text-stroke: 0.15px var(--hover-border-color);
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  }

  .back-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 1px;
    background-color: var(--hover-border-color);
    transition: width 0.3s ease;
  }

  .back-link:hover::after {
    width: 100%;
  }

  /* Modal Styles */
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
    max-width: 400px;
    width: 90%;
    text-align: center;
    border: 1px solid #d0cbc4;
  }

  .error-title {
    color: #423125;
    font-weight: 600;
    margin-bottom: 15px;
    font-size: 1.5rem;
  }

  .modal-content p {
    color: #423125;
    margin-bottom: 20px;
    font-size: 1.1rem;
  }

  .modal-button {
    display: inline-block;
    padding: 8px 20px;
    background-color: #423125;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
  }

  .modal-button:hover {
    background-color: #2a1f18;
  }

  /* Crop Modal Styles */
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
    /* background-color: #f4ebe2; */
    border-radius: 12px;
    /* padding: 20px; */
    display: flex;
    flex-direction: column;
  }

  .crop-viewport {
    width: 100%;
    height: 500px; /* Fixed height for the viewport */
    position: relative;
  }

  .crop-scroll-container {
    overflow: auto;
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Align to top for short images */
  }

  .crop-container {
    width: 700px;
    height: 500px;
    position: relative;
    overflow: hidden; /* Prevent anything from extending beyond container */
    border-radius: 10px;
  }

  /* Force cropper container dimensions */
  .crop-container >>> .cropper-container {
    width: 100% !important;
    height: 100% !important;
    overflow: hidden !important;
  }

  .crop-container >>> .cropper-canvas {
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    max-height: none !important;
  }

  .crop-container >>> .cropper-crop-box {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
  }

  .crop-container >>> .cropper-crop-box,
  .crop-container >>> .cropper-canvas,
  .crop-container >>> .cropper-img {
    max-width: none !important; /* Allow natural image sizing */
    max-height: none !important;
    overflow: visible !important;
  }

  .crop-controls {
    display: flex;
    justify-content: space-between;
    /* position: absolute; */
    bottom: 20px;
    left: 0;
    right: 0;
    padding: 0 20px;
    padding-top: 15px;
    z-index: 10;
  }


  .crop-container:active {
    cursor: grabbing;
  }

  .cropper-background {
    background-color: #f4ebe2;
    cursor: grab;
  }

  .cropper-background:active {
    cursor: grabbing;
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

  .fixed-crop-container {
    width: 700px;
    height: 500px;
    margin: 0 auto;
    position: relative;
    background-color: #f4ebe2;
  }

  .cropper-container {
    width: 100% !important;
    height: 100% !important;
  }

  @media (max-width: 768px) {
    .add-item-container {
      padding: 25px 20px;
    }

    .crop-modal-content {
      width: 95vw;
      height: 95vh;
    }
    
    .crop-container {
      width: 90vw;
      height: 90vw;
      max-width: 400px;
      max-height: 400px;
    }
    
    .crop-container >>> .cropper-container {
      width: 100% !important;
      height: 100% !important;
    }

    .crop-viewport {
      height: 60vh; /* Adjust for mobile */
    }

    .fixed-crop-container {
      width: 90vw;
      height: 90vw; /* Square aspect ratio */
      max-width: 400px;
      max-height: 400px;
    }
  }
</style>