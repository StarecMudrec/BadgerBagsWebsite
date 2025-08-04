<template>
  <div 
    class="bag-card"
    :class="{ 
      'selected': isSelected,
      'selected-animation': isSelected && !isMobile
    }"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <img 
      :src="'/bags_imgs/' + bag.image" 
      alt="Bag Image" 
      class="bag-image"
      @click="goToDetail"
    />
    <div class="bag-price">{{ bag.price }}₽</div>
    <input
      type="checkbox"
      class="selection-checkbox"
      :checked="isSelected"
      @change="handleCheckboxChange"
      @click.stop
    >
  </div>
</template>

<script>
export default {
  props: {
    bag: {
      type: Object,
      required: true,
      validator: (bag) => {
        return typeof bag.id !== 'undefined' && typeof bag.image !== 'undefined'
      }
    }
  },
  data() {
    return {
      isSelected: false,
      isMobile: false,
      isHovered: false
    };
  },
  mounted() {
    this.checkMobile();
    window.addEventListener('resize', this.checkMobile);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkMobile);
  },
  methods: {
    checkMobile() {
      this.isMobile = window.innerWidth <= 768;
    },
    goToDetail() {
      if (this.isSelected) return;
      if (!this.bag?.id) {
        console.error('Bag ID is missing', this.bag);
        return;
      }
      this.$router.push({ 
        name: 'BagDetail', 
        params: { id: this.bag.id.toString() }
      });
    },
    handleCheckboxChange(event) {
      this.isSelected = event.target.checked;
      this.$emit('bag-selected', this.bag.id, this.isSelected);
    }
  }
};
</script>

<style scoped>
.bag-card {
  padding: 10px;
  margin: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
  position: relative;
  transition: transform 0.3s ease;
}

.bag-card.selected {
  border: 4px solid rgba(255, 42, 42, 0.32);
  z-index: 10;
}

.bag-card.selected, 
.bag-card:hover {
  transform: translateY(-5px);
}

.bag-image {
  width: 100%;
  height: 100%;
  aspect-ratio: 1 / 1.56630057630;
  margin-bottom: 10px;
  box-shadow: 2px 4px 5px rgba(0, 0, 0, 0.24);
  border-radius: 4px;
  object-fit: cover;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.bag-card.selected .bag-image {
  transform: none; /* Disable individual image transform when card is selected */
}

.bag-card.selected-animation {
  animation: subtle-shake 5s infinite;
  animation-timing-function: ease-in-out;
}

@keyframes subtle-shake {
  0%, 90%, 100% {
    transform: translateY(-5px) rotate(0deg);
  }
  92% {
    transform: translateY(-5px) translateX(-3px) rotate(-1.5deg);
  }
  94% {
    transform: translateY(-5px) translateX(4px) rotate(2deg);
  }
  96% {
    transform: translateY(-5px) translateX(-2px) rotate(-1deg);
  }
  98% {
    transform: translateY(-5px) translateX(1px) rotate(0.5deg);
  }
}

.bag-price {
  font-weight: bold;
  color: #423125;
  font-size: 24px;
  font-family: 'Aclonica', sans-serif;
  pointer-events: none;
}

.selection-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 1;
  width: 20px;
  height: 20px;
  cursor: pointer;
  display: none;
}

@media (min-width: 769px) {
  .selection-checkbox {
    display: block;
  }
}

@media (max-width: 768px) {
  .selection-checkbox {
    display: block;
  }
  .bag-card.selected-animation {
    animation: none;
  }
}

@media (max-width: 480px) {
  .selection-checkbox {
    width: 30px;
    height: 30px;
  }
}
</style>