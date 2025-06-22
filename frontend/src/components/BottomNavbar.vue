<template>
  <nav class="bottom-navbar">
    <button class="navbar-button">О нас</button>
    <button class="navbar-button telegram-button">
      Телеграм
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" class="telegram-icon">
        <path fill="currentColor" d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm8.03 8.93l-2.81 13.15c-.27 1.26-.98 1.58-1.61 1.04l-3.92-2.89-1.86 1.82c-.27.27-.5.5-.96.5-.74 0-.66-.32-.92-.83l-1.4-4.22-3.52-2.15c-1.06-.65-.18-1.01 1.38-.52l8.79 5.36c1.03.63 1.92.33 2.22-.9l2.82-13.21c.33-1.61-.52-2.21-1.58-1.75z"/>
      </svg>
    </button>
  </nav>
</template>

<script>
export default {
  name: 'BottomNavbar'
}
</script>

<style scoped>
.bottom-navbar {
  width: 100%;
  background-color: #D4CBC2;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
}

.navbar-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  color: #333; /* Adjust color as needed */
  display: flex;
  align-items: center;
}

.telegram-button .telegram-icon {
  width: 20px; /* Adjust size as needed */
  height: 20px; /* Adjust size as needed */
  margin-left: 5px;
}
</style>