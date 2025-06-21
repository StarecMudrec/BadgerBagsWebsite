<template>
  <div class="menu">
    <router-link to="/" class="nav-btn">CARDS</router-link>
    <router-link to="/termins" class="nav-btn">TERMINS</router-link>
    <a v-if="isAuthenticated" href="/auth/logout" class="nav-btn" @click.prevent="logout">LOGOUT</a>
    <router-link v-else to="/login" class="nav-btn">LOGIN</router-link>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    ...mapState(['isAuthenticated'])
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logout')
      // Перенаправление уже обрабатывается в роутере
    }
  }
}
</script>

<style scoped>
.menu {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 30px 0 20px 0;
  left: 0;
  top: 0;
  padding: 0;
  position: fixed;
  z-index: 100;
  /* background: linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%); */
  width: 100%;
  pointer-events: none; /* This makes the entire menu click-through */
}

/* Add a pseudo-element for the gradient background */
.menu::before {
  content: '';
  position: absolute;
  top: -30px; /* Compensate for top margin */
  left: 0;
  right: 0;
  bottom: -20px; /* Compensate for bottom margin */
  background: linear-gradient(to bottom, rgba(0,0,0,0.57) 0%, rgba(0,0,0,0) 100%);
  z-index: -1;
  width: 100%;
  pointer-events: none; /* Make the gradient click-through too */
}

.nav-btn {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 25px; /* Increased font size */
  letter-spacing: 1px; /* Slightly increased letter spacing for better readability with outline */
  position: relative;
  padding: 5px 0;
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
  pointer-events: auto; /* But make the buttons clickable */
}

.nav-btn:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
  transition: color 0.3s ease, box-shadow 0.3s ease; /* Add box-shadow to transition */
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Semi-transparent dark shadow */
}

.nav-btn::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-color);
  transition: width 0.3s ease;
}

.nav-btn:hover::after {
  width: 100%;
}

@media (max-width: 480px) {
  .menu {
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .nav-btn {
    font-size: 16px;
  }
}
</style>
