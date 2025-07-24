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
import { mapState, mapActions } from 'vuex'

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
    ...mapActions(['logout']),
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600&family=Noto+Serif:ital,wght@0,400;0,500;1,400&display=swap');

.menu-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 20px; /* Small hover area at top of screen */
  z-index: 100;
  pointer-events: auto; /* Enable hover detection */
}

.menu {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 0;
  left: 0;
  top: 0;
  padding: 30px 0 20px 0;
  position: fixed;
  width: 100%;
  transition: transform 0.3s ease, padding 0.3s ease, background-color 0.3s ease;
  z-index: 101;
}

.menu-hidden {
  transform: translateY(-100%);
  padding-top: 10px;
  padding-bottom: 10px;
  pointer-events: none; /* Make hidden menu click-through */
}

/* Buttons should always be clickable when menu is visible */
.menu:not(.menu-hidden) .nav-btn {
  pointer-events: auto;
}

/* Add a pseudo-element for the gradient background */
.menu::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.57) 0%, rgba(0,0,0,0) 100%);
  z-index: -1;
  width: 100%;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.menu-hidden::before {
  opacity: 0;
}

.nav-btn--current {
  color: var(--hover-color);
  cursor: default;
  /* -webkit-text-stroke: 0.15px var(--hover-border-color); */
}

.nav-btn--current::after {
  /* width: 100% !important; */
}

.nav-btn {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
  font-size: 25px;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  letter-spacing: 1px;
  position: relative;
  padding: 5px 0;
  transition: color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.nav-btn:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px var(--hover-border-color);
  transition: color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}

.nav-btn::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: var(--hover-border-color);
  transition: width 0.3s ease;
}

.nav-btn:hover::after {
  width: 100%;
}

@media (max-width: 480px) {
  .menu-wrapper {
    height: 15px;
  }
  
  .menu {
    gap: 20px;
    padding-bottom: 30px;
  }
  
  .nav-btn {
    font-size: 16px;
  }
}
</style>