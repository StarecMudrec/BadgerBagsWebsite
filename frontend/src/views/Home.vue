<template>
  <div>
    <div class="background-container"></div>
    <hr class="separator-line">
    <div class="bag-catalog">
      <BagCard v-for="bag in bags" :key="bag.id" :bag="bag" />
    </div>
  </div>
</template>
<style scoped>
  width: 100%;  
 height: 100vh; /* Adjust height as needed */
  background-image: url('/background.jpg');
  background-size: cover;
  background-position: center 57%; /* Position the vertical center 80% down from the top, center horizontally */
  bottom: 0; /* Anchor to the bottom */
}
.separator-line {
  position: absolute;
  bottom: 0; /* Position at the bottom edge of the background container */
  left: 0;
  height: 4px;
  width: 100%;  background-color: white;
  z-index: 2; /* Ensure it's above the background */
}
.error-message {
  position: relative; /* Ensure it's positioned relative to the flow */
  text-align: center;
  margin: 50px 0;
  color: #ff5555; /* Red color for errors */
}
page-container {
  position: relative;
  min-height: 100vh;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 400px); /* Учитываем высоту хедера */
}


.bag-catalog {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); /* Adjust minmax for card size */
  gap: 20px; /* Adjust gap between cards */
  padding: 20px;
  margin-top: 100vh; /* Push the catalog down below the background image */
  background-color: #e0d8ce; /* Match the background color from the image */
}

</style>

<script>
import BagCard from '@/components/BagCard.vue' // Import BagCard component
import axios from 'axios'; // Import axios
export default {
  components: {
    BagCard // Register BagCard component
  },

  data() {
    return {
      isUserAllowed: false,
      bags: [] // Add bags data property
    };
  },

  methods: {
    navigateToCard(cardUuid) { // Deprecated - use @card-clicked on card component directly
      this.$router.push(`/card/${cardUuid}`);
    },
    updateUserAllowedStatus(isAllowed) {
      console.log('Received user allowed status:', isAllowed);
      this.isUserAllowed = isAllowed;
    },
    navigateToAddCard() {
    },
    async fetchBagData() { // Add method to fetch bag data
      try {
        const response = await axios.get('/api/bags');
        this.bags = response.data;
      } catch (error) {
        console.error('Error fetching bag data:', error);
      }
    }
  },
  mounted() {
    this.fetchBagData(); // Call fetchBagData in mounted hook
  },
  // Add a new method to handle season deletion
  handleSeasonDeleted(deletedSeasonUuid) {
    // Call the mutation to remove the season from the VueX store
    this.REMOVE_SEASON(deletedSeasonUuid);
  }
}
</script>