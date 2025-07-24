<template>
  <div class="menu-wrapper" @mouseenter="showMenu" @mouseleave="hideMenu">
    <div class="menu" :class="{ 'menu-hidden': isHidden }">
      <template v-if="$route.path === '/'">
        <span class="nav-btn nav-btn--current">КАТАЛОГ</span>
      </template>
      <template v-else>
        <router-link to="/" class="nav-btn">КАТАЛОГ</router-link>
      </template>
      <template v-if="$route.path === '/about'">
        <span class="nav-btn nav-btn--current">О НАС</span>
      </template>
      <template v-else>
        <router-link to="/about" class="nav-btn">О НАС</router-link>
      </template>
      <!-- Add this new logout button -->
      <a v-if="user?.is_admin" href="/auth/logout" class="nav-btn logout-btn" @click.prevent="logout">
        ВЫЙТИ
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="logout-icon">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
          <polyline points="16 17 21 12 16 7"></polyline>
          <line x1="21" y1="12" x2="9" y2="12"></line>
        </svg>
      </a>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  props: {
    user: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isHidden: false,
      lastScrollPosition: 0,
      hideTimeout: null
    }
  },
  computed: {
    ...mapState(['isAuthenticated'])
  },
  methods: {
    async logout() {
      try {
        const response = await fetch('/auth/logout', {
          method: 'POST'
        });
        if (response.ok) {
          window.location.href = '/'; // Refresh the page to update auth state
        }
      } catch (error) {
        console.error('Logout error:', error);
      }
    },
    onScroll() {
      const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop
      if (currentScrollPosition < 0) return
      
      if (Math.abs(currentScrollPosition - this.lastScrollPosition) < 60) return
      
      this.isHidden = currentScrollPosition > this.lastScrollPosition && currentScrollPosition > 100
      this.lastScrollPosition = currentScrollPosition
    },
    showMenu() {
      clearTimeout(this.hideTimeout)
      this.isHidden = false
    },
    hideMenu() {
      if (window.pageYOffset > 100) {
        this.hideTimeout = setTimeout(() => {
          this.isHidden = true
        }, 300)
      }
    }
  },
  mounted() {
    window.addEventListener('scroll', this.onScroll)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.onScroll)
    clearTimeout(this.hideTimeout)
  }
}
</script>

<style scoped>
/* Add to existing styles */
.logout-btn {
  margin-left: auto; /* Pushes the button to the right */
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.logout-btn:hover .logout-icon {
  transform: translateX(2px);
}

/* Adjust menu to allow space for logout button */
.menu {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 0;
  left: 0;
  top: 0;
  padding: 30px 40px 20px 40px; /* Increased padding on sides */
  position: fixed;
  width: 100%;
  transition: transform 0.3s ease, padding 0.3s ease, background-color 0.3s ease;
  z-index: 101;
}
</style>