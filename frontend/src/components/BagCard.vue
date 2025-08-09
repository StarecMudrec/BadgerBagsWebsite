<template>
  <div 
    class="bag-card"
    :class="{ 'selected': isSelected }"
    @click="handleCardClick"
  >
    <img 
      :src="'/bags_imgs/' + bag.image" 
      alt="Bag Image" 
      class="bag-image"
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
    },
    selectionMode: { // Add this prop
      type: Boolean,
      default: false
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
    handleCardClick() {
      if (this.selectionMode || this.isSelected) {
        this.toggleSelection();
      } else {
        this.goToDetail();
      }
    },
    toggleSelection() {
      this.isSelected = !this.isSelected;
      this.$emit('bag-selected', this.bag.id, this.isSelected);
    },
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
  /* padding: 10px; */
  margin: 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
  position: relative;
  box-sizing: border-box;
  /* border: 4px solid transparent; */
  cursor: pointer;
  aspect-ratio: 1 / 1.67; /* Adjusted ratio to make space for price */
  box-shadow: 2px 4px 5px rgba(0, 0, 0, 0.24);
}

.bag-card.raised {
  transform: translateY(-15px); /* Raise effect */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); /* Enhanced shadow when raised */
}

.bag-card.selected {
  border: 4px solid rgba(255, 42, 42, 0.32);
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
  z-index: 1;
  filter: blur(4px);
  border-radius: 8px; /* Match card's rounded corners */
}

.bag-card.selected-animation {
  animation: ominous-shake 4s infinite;
  animation-timing-function: ease-in-out;
}

@keyframes ominous-shake {
  0%, 85%, 100% {
    transform: translateY(-15px) rotate(0deg); /* Maintain raised position */
  }
  88% {
    transform: translateY(-15px) translateX(-6px) rotate(-3deg); /* Shake left */
  }
  90% {
    transform: translateY(-15px) translateX(8px) rotate(4deg); /* Shake right */
  }
  92% {
    transform: translateY(-15px) translateX(-4px) rotate(-2deg); /* Shake left */
  }
  94% {
    transform: translateY(-15px) translateX(3px) rotate(1deg); /* Shake right */
  }
  96% {
    transform: translateY(-15px) translateX(-2px) rotate(-0.5deg); /* Settle */
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
  height: auto; /* Changed from 100% to auto */
  aspect-ratio: 1 / 1.56630057630; /* Maintain original image ratio */
  margin-bottom: 5px;
  border-radius: 4px;
  object-fit: cover;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* .bag-card:hover .bag-image {
  transform: translateY(-5px);
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