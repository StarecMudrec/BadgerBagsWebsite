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
  box-sizing: border-box;
  border: 4px solid transparent;
  transform: translateY(0);
  will-change: transform, box-shadow; /* Optimize for animation */
  transition: 
    transform 0.5s cubic-bezier(0.23, 1, 0.32, 1),
    box-shadow 0.5s cubic-bezier(0.23, 1, 0.32, 1),
    border-color 0.3s ease;
  z-index: 1;
}

.bag-card.raised {
  transform: translateY(-15px); /* Raise effect */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* Enhanced shadow when raised */
}

.bag-card.selected {
  transform: translateY(-15px);
  border-color: rgba(255, 42, 42, 0.32);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  z-index: 2; /* Ensure selected card appears above others */
}

.bag-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.bag-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: transparent; /* Start transparent */
  z-index: 0;
  filter: blur(4px);
  transition: background-color 0.2s ease; /* Add transition */
}

.bag-card.selected::before {
  content: '';
  position: absolute;
  top: -4px; /* Account for border */
  left: -4px;
  right: -4px;
  bottom: -4px;
  background-color: rgba(255, 42, 42, 0.24);
  z-index: -1;
  filter: blur(8px);
  opacity: 0;
  transition: opacity 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

.bag-card.selected::before {
  opacity: 1;
}

.bag-card.selected-animation {
  animation: 
    float 3s ease-in-out infinite,
    ominous-shake 8s infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(-15px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes ominous-shake {
  0%, 90%, 100% {
    transform: translateY(-15px) rotate(0deg);
  }
  92% {
    transform: translateY(-15px) translateX(-3px) rotate(-1.5deg);
  }
  94% {
    transform: translateY(-15px) translateX(4px) rotate(2deg);
  }
  96% {
    transform: translateY(-15px) translateX(-2px) rotate(-1deg);
  }
  98% {
    transform: translateY(-15px) translateX(1px) rotate(0.5deg);
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
  transition: all 0.3s ease;
  opacity: 0;
}

.bag-card:hover .selection-checkbox,
.bag-card.selected .selection-checkbox {
  opacity: 1;
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

/* .bag-image:hover {
  transform: scale(1.02);
}

.bag-card.selected .bag-image:hover {
  transform: none;
} */

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
  .bag-card.selected {
    transform: translateY(-8px);
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