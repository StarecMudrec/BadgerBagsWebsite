<template>
  <div class="bag-card" @click="goToDetail">
    <img :src="'/bags_imgs/' + bag.image" alt="Bag Image" class="bag-image" />
    <div class="bag-price">{{ bag.price }}₽</div>
  </div>
</template>

<script>
export default {
  props: {
    bag: {
      type: Object,
      required: true
    }
  },
  methods: {
    goToDetail() {
      this.$router.push({ name: 'BagDetail', params: { id: this.bag.id } });
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
}

.bag-image {
  max-width: 100%;
  height: 100%;
  margin-bottom: 10px;
  box-shadow: 2px 4px 5px rgba(0, 0, 0, 0.24);
  border-radius: 4px;
  object-fit: cover;
  overflow: hidden;
}

.bag-price {
  font-weight: bold;
  color: #423125;
  font-size: 24px;
  font-family: 'Aclonica', sans-serif;
}
</style>