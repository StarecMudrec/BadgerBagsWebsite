<template>
  <div class="bag-card">
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
  height: auto;
  margin-bottom: 10px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

.bag-price {
  font-weight: bold;
  color: #423125;
}
</style>