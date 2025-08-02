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
            :min-container-width="500"
            :min-container-height="500"
            :max-container-width="1000"
            :max-container-height="1000"
            :ready="initializeCropper"
            guides
            background-class="cropper-background"
          ></vue-cropper>
        </div>
        <div class="crop-controls">
          <button @click="cancelCrop" class="crop-button cancel">Cancel</button>
          <button @click="applyCrop" class="crop-button confirm">Apply Crop</button>
        </div>
      </div>
    </div>

    <div class="add-item-container">
      <h1>Add New Bag</h1>
      <form @submit.prevent="submitForm" class="item-form">
        <div class="form-group">
          <label for="name">Bag Name:</label>
          <input type="text" id="name" v-model="item.name" required>
        </div>
        
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea id="description" v-model="item.description" required></textarea>
        </div>
        
        <div class="form-group">
          <label for="price">Price (₽):</label>
          <input type="number" id="price" v-model.number="item.price" required>
        </div>
        
        <div class="form-group file-upload-group">
          <label for="image" class="file-upload-label">
            <span class="file-upload-text">
              {{ item.image ? item.image.name : 'Choose bag image...' }}
            </span>
            <span class="file-upload-button">Browse</span>
            <input 
              type="file" 
              id="image" 
              @change="handleFileUpload" 
              accept="image/*" 
              required
              class="file-upload-input"
            >
          </label>
        </div>
        
        <button type="submit" class="submit-button">
          <span class="submit-button-text">Add Bag</span>
        </button>
      </form>
      
      <router-link to="/" class="back-link">← Back to home</router-link>
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
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imageToCrop = e.target.result;
          this.showCropModal = true;
          this.$nextTick(() => {
            if (this.$refs.cropper) {
              this.$refs.cropper.replace(e.target.result);
              // Set initial zoom to fit the image in the viewport
              this.$refs.cropper.zoomTo(0.5);
            }
          });
        };
        reader.readAsDataURL(file);
      }
    },
    initializeCropper() {
      // Set fixed container dimensions
      const container = this.$refs.cropper.$el.parentElement;
      container.style.width = '500px';
      container.style.height = '500px';
      
      // Reset cropper with new dimensions
      this.$refs.cropper.reset();
      
      // Zoom to fit image in container
      this.$refs.cropper.zoomTo(0.5);
    },
    onCropperReady() {
      // Adjust container height to match the image height
      const container = this.$refs.cropper.$el.parentElement;
      const imgHeight = this.$refs.cropper.$el.querySelector('img').naturalHeight;
      this.containerHeight = `${Math.min(imgHeight, window.innerHeight * 0.7)}px`;
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
      if (!this.item.image) {
        this.errorMessage = 'Please select an image file.';
        this.showErrorModal = true;
        return;
      }

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
}

h1 {
  text-align: center;
  color: #423125;
  font-size: 2.2rem;
  margin-bottom: 30px;
  font-weight: 600;
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
  font-weight: 500;
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
  padding: 14px;
  background-color: #423125;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 500;
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
  padding: 20px;
}

.crop-modal-content {
  background-color: #f4ebe2;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 20px;
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
  width: 100%;
  height: 100%;
}

.crop-controls {
  display: flex;
  justify-content: space-between;
  padding: 15px 0 0 0;
  background-color: transparent;
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
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.crop-button.cancel {
  background-color: #d0cbc4;
  color: #423125;
}

.crop-button.cancel:hover {
  background-color: #c5beb6;
}

.crop-button.confirm {
  background-color: #423125;
  color: white;
}

.crop-button.confirm:hover {
  background-color: #2a1f18;
}

.fixed-crop-container {
  width: 500px;
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
    height: calc(95vh - 70px);
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