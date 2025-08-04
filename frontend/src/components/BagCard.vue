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
  transform: translateY(0) scale(1);
  transition: 
    transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94),
    border-color 0.3s ease,
    box-shadow 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  will-change: transform;
  z-index: 1;
}

.bag-card.raised {
  transform: translateY(-15px); /* Raise effect */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* Enhanced shadow when raised */
}

.bag-card.selected {
  border-color: rgba(255, 42, 42, 0.32);
  transform: translateY(-15px) scale(1.02);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
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
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background-color: rgba(255, 42, 42, 0.24);
  z-index: -1;
  filter: blur(6px);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.bag-card.selected::before {
  opacity: 1;
}

.bag-card.selected-animation {
  animation: float-shake 6s infinite ease-in-out;
}

@keyframes float-shake {
  0%, 100% {
    transform: translateY(-15px) scale(1.02) rotate(0deg);
  }
  50% {
    transform: translateY(-18px) scale(1.02) rotate(0.5deg);
  }
  10%, 30%, 70%, 90% {
    transform: translateY(-15px) scale(1.02) rotate(0deg);
  }
  20% {
    transform: translateY(-15px) scale(1.02) translateX(-3px) rotate(-1deg);
  }
  40% {
    transform: translateY(-15px) scale(1.02) translateX(2px) rotate(0.8deg);
  }
  60% {
    transform: translateY(-15px) scale(1.02) translateX(-1px) rotate(-0.5deg);
  }
  80% {
    transform: translateY(-15px) scale(1.02) translateX(1px) rotate(0.3deg);
  }
}

.bag-card:not(.selected):hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transition: 
    transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94),
    box-shadow 0.3s ease;
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
  .bag-card.selected {
    transform: translateY(-8px) scale(1.01);
  }
  
  .bag-card.selected-animation {
    animation: none;
  }
  
  @keyframes float-shake {
    0%, 100% {
      transform: translateY(-8px) scale(1.01);
    }
    50% {
      transform: translateY(-10px) scale(1.01);
    }
  }
}

@media (max-width: 480px) {
  .selection-checkbox {
    width: 30px;
    height: 30px;
  }
}
</style>