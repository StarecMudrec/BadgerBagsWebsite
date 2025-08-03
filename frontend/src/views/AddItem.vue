<template>
  <div class="add-item-page">
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
        <div class="crop-container">
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
            guides
            background-class="cropper-background"
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
        
        <div class="form-group file-upload-group" :class="{ 'has-error': fileError }">
          <label for="image" class="file-upload-label">
            <span class="file-upload-text">
              {{ item.image ? item.image.name : 'Загрузите фото...' }}
            </span>
            <span class="file-upload-button">Загрузить</span>
            <input 
              type="file" 
              id="image" 
              @change="handleFileUpload" 
              accept="image/*"
              class="file-upload-input"
            >
          </label>
          <span v-if="fileError" class="error-message">Пожалуйста, загрузите фото</span>
        </div>
        
        <button 
          type="submit" 
          :disabled="isSubmitting"
          class="submit-button"
        >
          <span v-if="!isSubmitting">Добавить</span>
          <span v-else>Добавляем...</span>
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

export default {
  name: 'AddItem',
  components: {
    VueCropper
  },
  data() {
    return {
      item: {
        name: '',
        description: '',
        price: null,
        image: null
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
      isSubmitting: false,  // Add this
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
    handleFileUpload(event) {
      const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB limit
      const file = event.target.files[0];
      this.fileError = false; // Reset error state

      // Check file size
      if (file.size > MAX_FILE_SIZE) {
        this.errorMessage = 'Image size must be less than 5MB.';
        this.showErrorModal = true;
        event.target.value = ''; // Clear the file input
        return;
      }
      
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          this.imageToCrop = e.target.result;
          this.showCropModal = true;
          await this.$nextTick();
          if (this.$refs.cropper) {
            this.$refs.cropper.replace(e.target.result);
            await this.initializeCropper();
          }
        };
        reader.readAsDataURL(file);
      } else {
        this.fileError = true;
      }
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
      // Set initial zoom boundaries
      this.$refs.cropper.setZoomRange({
        min: 0.1,  // Minimum zoom level (10%)
        max: 2.0   // Maximum zoom level (200%)
      });
      
      // Set initial zoom to fit image nicely
      this.$refs.cropper.zoomTo(0.5);
      
      // Prevent zooming beyond boundaries
      this.$refs.cropper.on('zoom', (event) => {
        const canvasData = this.$refs.cropper.getCanvasData();
        const containerData = this.$refs.cropper.getContainerData();
        
        // Prevent zooming in too far
        if (canvasData.width < containerData.width || 
            canvasData.height < containerData.height) {
          this.$refs.cropper.zoomTo(1.0); // Reset to 100% if too small
        }
      });
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
      document.getElementById('image').value = '';
    },
    applyCrop() {
      this.$refs.cropper.getCroppedCanvas().toBlob(async (blob) => {
        const fileName = 'cropped_' + Date.now() + '.png'; // Unique filename
        this.item.image = new File([blob], fileName, { type: 'image/png' });
        
        // Preview the cropped image
        this.croppedPreview = URL.createObjectURL(blob);
        this.showCropModal = false;
      }, 'image/png');
    },
    closeModal() {
      this.showErrorModal = false;
      this.errorMessage = '';
    },
    async submitForm() {
      if (this.isSubmitting) return;  // Prevent duplicates
      
      this.isSubmitting = true;
      // Manual validation for file input
      if (!this.item.image) {
        this.errorMessage = 'Please select an image file.';
        this.showErrorModal = true;
        return;
      }

      // Rest of your existing submit logic
      try {
        const formData = new FormData();
        formData.append('name', this.item.name);
        formData.append('description', this.item.description);
        formData.append('price', this.item.price);
        formData.append('img', this.item.image);

        const response = await axios.post('/api/bags', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        this.$router.push('/');
      } catch (error) {
        this.errorMessage = 'Error adding bag: ' + 
          (error.response?.data?.error || error.message);
        this.showErrorModal = true;
        console.error('Error details:', error.response);
      } finally {
        this.isSubmitting = false;  // Re-enable button
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
.add-item-page {
  position: relative;
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(to bottom, #f3efeb 0%, #e7e2dc 100%);
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
}

.add-item-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  margin-top: 70px;
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
  width: 100%;
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
  color: #423125;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #2a1f18;
  text-decoration: underline;
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
  
  h1 {
    font-size: 1.8rem;
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