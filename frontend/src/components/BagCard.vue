<template>
  <div class="bag-card">
    <img 
      :src="'/bags_imgs/' + bag.image" 
      alt="Bag Image" 
      class="bag-image"
      @click="goToDetail"
    />
    <div class="bag-price">{{ bag.price }}₽</div>
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
  methods: {
    goToDetail() {
      if (!this.bag?.id) {
        console.error('Bag ID is missing', this.bag);
        return;
      }
      this.$router.push({ 
        name: 'BagDetail', 
        params: { id: this.bag.id.toString() }
      });
    }
  }
};
</script>

<style scoped>
.bag-card {
  /* border: 1px solid #ccc; */
  padding: 10px;
  margin: 10px;
  text-align: center;
  /* background-color: #fff; */
  /* box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); */
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%; /* Add this */
  width: 100%; /* Add this */
}

.bag-image {
  width: 100%;
  height: 100%;
  aspect-ratio: 1 / 1.56630057630; /* Match the same ratio as add-item-button */
  margin-bottom: 10px;
  box-shadow: 2px 4px 5px rgba(0, 0, 0, 0.24);
  border-radius: 4px;
  object-fit: cover;
  overflow: hidden;
  cursor: pointer; /* Add pointer cursor to indicate clickability */
  transition: transform 0.2s ease; /* Optional: Add hover effect */
}

.bag-image:hover {
  transform: scale(1.02); /* Optional: Slight zoom on hover */
}

.bag-price {
  font-weight: bold;
  color: #423125;
  font-size: 24px;
  font-family: 'Aclonica', sans-serif;
  pointer-events: none; /* Prevent any pointer events on price */
}
</style>