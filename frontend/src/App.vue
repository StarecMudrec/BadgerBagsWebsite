<template>
  <div id="app">
    <Navbar :user="user"/>
    <router-view v-slot="{ Component, route }">
      <div class="router-view-container">
        <transition name="fade" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </transition>
      </div>
    </router-view>
  </div>
</template>

<script>
import axios from 'axios'; // Import axios
import Navbar from '@/components/Navbar.vue';
// import BottomNavbar from '@/components/BottomNavbar.vue'; // Import the new component
import router from './router'; // Import router

export default {
  name: 'App', components: {
    Navbar, 
    // BottomNavbar
  },
  computed: {
    ...mapState(['user'])
  },
  async created() {
    await this.$store.dispatch('checkAuth')
  },
  data() {
    return {
      user: null // Initialize user data to null
    };
  },
  mounted() {
    // Make a GET request to the user endpoint on component mount
    axios.get('/api/user')
      .then(response => {
        if (response.status === 200 && response.data) {
          this.user = response.data; // Set the user data if authenticated
        } else {
          this.user = null; // Ensure user is null if not authenticated
        }
      })
      .catch(error => {
        console.error('Error fetching user data:', error);
        this.user = null; // Ensure user is null on error
      });
  },
}
</script>

<style>
/* Глобальные стили */
:root {
  --bg-color: #dfd9d2;
  --card-bg: #1e1e1e;
  --text-color: #e0e0e0;
  --accent-color: #ffffff;
  --hover-color: #b4aaa3;
  --hover-border-color: #a69d96;
  --card-border-color:  #bebebe;
}

html {
  margin: 0;
  padding: 0;
  height: 100%;
  background-color: var(--bg-color);
}

.global-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  align-items: center;
  margin: 0;
}
/* Глобальные стили для всех элементов */

* {
  box-sizing: border-box;
}
/* Анимации переходов */

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.user-info {

  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  align-items: center;
  color: var(--text-color);
  font-size: 14px;
  z-index: 10; /* Ensure user info is above other elements */
}

.user-info .avatar {

  width: 30px;
  height: 30px;
  border-radius: 50%; /* Make the avatar round */
  margin-right: 10px;
  border: 1px solid var(--border-color);
  object-fit: cover; /* Ensure the image covers the area without distortion */
}

button, .button {

  padding: 10px 15px; /* Increased padding for larger buttons */
}
</style>
