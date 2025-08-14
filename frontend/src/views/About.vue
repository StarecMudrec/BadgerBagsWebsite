<template>
  <div class="about-page">
    <!-- Background portrait image -->
    <div class="portrait-background"></div>
    
    <!-- Main content section -->
    <div class="about-content">
      <div class="content-wrapper">
        <div class="about-section">
          <h2 class="section-title">Обо мне:</h2>
          <p class="section-text">Здесь будет находиться информация о вас и ваших сумках</p>
        </div>
      </div>
    </div>
    
    <!-- Bottom navigation -->
    <nav class="bottom-navbar">
      <a href="https://t.me/StarecMudrec" class="navbar-button telegram-button" target="_blank">
        ОТЗЫВЫ
        <!-- <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="24" height="24" class="telegram-icon">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
        </svg> -->
      </a>
      <a href="https://t.me/kurorooooo" class="navbar-button telegram-button" target="_blank">
        ТЕЛЕГРАМ
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="24" height="24" class="telegram-icon">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
        </svg>
      </a>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700;900&family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Cormorant+Garamond:wght@400;500;600;700&display=swap');

.about-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(to bottom, #dad4ce 0%, #f4ebe2 100%);
  overflow: hidden;
}

.portrait-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 40%; 
  height: 100vh;
  background-image: url('/portrait.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: 0;
}

.about-content {
  position: relative;
  flex: 1;
  width: 60%; 
  margin-left: 40%; 
  padding: 40px 10% 40px 12%; 
  z-index: 1;
  background: transparent;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content-wrapper {
  width: 90%;
  max-width: 700px; 
  align-self: center;
}

.about-section {
  margin-bottom: 40px;
}

.section-title {
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 1000;
  font-size: 3rem;
  color: #423125;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 1px solid #a69d96;
  width: 100%;
  letter-spacing: 0.5px;
}

.section-text {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 700;
  font-size: 1.8rem;
  line-height: 1.7;
  color: #423125;
  letter-spacing: 0.2px;
}

.bottom-navbar {
  position: relative;
  width: 60%; 
  margin-left: 40%; 
  display: flex;
  justify-content: space-around;
  padding: 15px 8%; 
  min-height: 85px;
  background: transparent;
  z-index: 2;
}

.navbar-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  display: flex;
  align-items: center;
  font-family: 'Noto Serif TC', 'Noto Serif', serif;
  font-weight: 1000;
  font-size: 26px;
  transition: color 0.3s ease;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
  position: relative;
  text-decoration: none;
  padding: 8px 15px;
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.navbar-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px #a69d96;
}

.navbar-button::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 1px;
  background-color: #a69d96;
  transition: width 0.3s ease;
  bottom: 5px;
}

.navbar-button:hover::after {
  width: 100%;
}

.telegram-button {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.telegram-button:hover {
  color: var(--hover-color);
  -webkit-text-stroke: 0.15px #a69d96;
}

.telegram-button:hover .telegram-icon {
  fill: var(--hover-color);
  transform: scale(1.1);
}

.telegram-icon {
  width: 30px;
  height: 30px;
  transition: all 0.3s ease;
  fill: #333333;
}

@media (max-width: 768px) {
  .portrait-background {
    width: 100%;
    height: 40vh;
    position: relative;
  }
  
  .about-content,
  .bottom-navbar {
    width: 100%;
    margin-left: 0;
    padding: 20px;
  }
  
  .section-title {
    font-size: 2.4rem;
  }
  
  .section-text {
    font-size: 1.5rem;
  }
  
  .navbar-button {
    font-size: 22px;
    padding: 6px 12px;
  }
  
  .telegram-icon {
    width: 26px;
    height: 26px;
  }
  
  .bottom-navbar {
    min-height: 75px;
    padding: 12px 20px;
  }
}
</style>