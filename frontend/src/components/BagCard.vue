<template>
  <div 
    class="bag-card"
    :class="{ 
      'selected': isSelected,
      'selected-animation': isSelected && !isMobile
    }"
  >
    <img 
      :src="'/bags_imgs/' + bag.image" 
      alt="Bag Image" 
      class="bag-image"
      @click="goToDetail"
      :class="{ 'selected': isSelected }"
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
      isMobile: false
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
  transform: translateY(-5px); /* Base rise transform */
  border: 4px solid rgba(255, 42, 42, 0.32);
  z-index: 10;
  animation: subtle-shake 5s infinite; /* Only handles the shake */
  animation-timing-function: ease-in-out;
}

.bag-card.selected::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 42, 42, 0.24);
  z-index: 0;
  filter: blur(4px);
}

.bag-card.selected-animation {
  animation: subtle-shake 5s infinite;
  animation-timing-function: ease-in-out;
}

@keyframes subtle-shake {
  0%, 90%, 100% {
    transform: translateY(-5px) rotate(0deg); /* Maintain base rise */
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
}

.bag-image:hover {
  transform: scale(1.02) translateY(-5px);
  transition: transform 0.3s ease;
}

.bag-card.selected .bag-image:hover {
  transform: none;
}

.bag-card.selected {
  transition: transform 0.3s ease, border 0.3s ease;
}

.bag-price {
  font-weight: bold;
  color: #423125;
  font-size: 24px;
  font-family: 'Aclonica', sans-serif;
  pointer-events: none;
}

@media (max-width: 768px) {
  .selection-checkbox {
    display: block;
  }
  .bag-card.selected-animation {
    animation: none;
    transform: none;
  }
}

@media (max-width: 480px) {
  .selection-checkbox {
    width: 30px;
    height: 30px;
  }
}
</style>