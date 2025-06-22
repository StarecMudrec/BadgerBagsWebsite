<template>
  <nav class="bottom-navbar">
    <button class="navbar-button">О нас</button>
    <button class="navbar-button telegram-button">
      Телеграм
      <img src="@/assets/telegram-icon.png" alt="Telegram Icon" class="telegram-icon" />
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
  position: fixed;
  bottom: 0;
  left: 0;
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