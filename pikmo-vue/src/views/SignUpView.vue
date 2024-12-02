<template>
  <div class="l-container">
    <!-- Background Carousel -->
    <div id="carouselExampleSlidesOnly" class="carousel slide background-img" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active" data-bs-interval="3000">
          <img src="https://image.tmdb.org/t/p/original/qJeU7KM4nT2C1WpOrwPcSDGFUWE.jpg" class="d-block w-100 carousel-img" alt="...">
        </div>
        <div class="carousel-item">
          <img src="https://image.tmdb.org/t/p/original/vy2HZLHvulytHEyqKBOniYx9GGx.jpg" class="d-block w-100 carousel-img" alt="...">
        </div>
        <div class="carousel-item">
          <img src="https://image.tmdb.org/t/p/original/s1sQrnAYGVUTWBP0Et776aDl7q3.jpg" class="d-block w-100 carousel-img" alt="...">
        </div>
      </div>
    </div>

    <!-- Wrapper with form and backdrop filter -->
    <div class="wrapper">
      <div class="signup-txt">Sign Up</div>
      <div class="signup-items">
        <form @submit.prevent="signUp" class="signup-form">
          <input class="username-input" type="text" id="username" v-model.trim="username" placeholder="Enter your username."><br>
          <input class="password-input" type="password" id="password1" v-model.trim="password1" placeholder="Enter your password."><br>
          <input class="password-input" type="password" id="password2" v-model.trim="password2" placeholder="Please re-enter your password."><br>
          <div class="ridio-items d-flex">
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="f" v-model="gender">
              <label class="form-check-label" for="inlineRadio1">Female</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="m" v-model="gender">
              <label class="form-check-label" for="inlineRadio2">Male</label>
            </div>
          </div>
          <input class="submit-btn" type="submit" value="Sign up">



        </form>
        <div class="login-txt">Already have account? <RouterLink :to="{ name: 'LogInView' }">Login.</RouterLink></div>
      </div>
    </div> 
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { RouterLink } from "vue-router";

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const gender = ref("f"); // 기본값을 여성('f')으로 설정

const store = useCounterStore();

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value,
  };
  store.signUp(payload);
};
</script>

<style scoped>
* {font-family: "Noto Sans KR", sans-serif;}

.l-container {
  position: relative;
  width: 100%;
  height: 100vh; /* 전체 화면을 덮기 위해 100vh로 설정 */
  overflow: hidden;
}

.background-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.carousel-img {
  object-fit: cover;
  width: 100%;
  height: 100vh;
}

.wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* justify-content: center; */
  justify-content: space-between;
  width: 27rem;
  height: 30rem;
  padding: 2.5rem;
  background-color: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px); /* 배경을 흐리게 처리 */
  border-radius: 15px;
  z-index: 1; /* wrapper가 배경 위에 보이도록 설정 */
  margin: auto; /* 화면 가운데에 배치 */
  top: 50%;
  transform: translateY(-50%);
  gap:10px
}

.signup-txt {
  /* margin-top: 1rem; */
  font-size: 2rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.username-input, .password-input {
  all: unset;
  padding: 10px 5px;
  border: none;
  border-bottom: 2px solid rgba(255,255,255,0.9);
  background: none;
  letter-spacing: 1px;
  font-weight:200;
}

.username-input {
  margin: 2rem 0 1rem 0;
}

.username-input::placeholder, .password-input::placeholder{
  color: rgba(255,255,255,0.9);
}

.username-input:focus, .password-input:focus {
  outline: none;
}

.submit-btn {
  margin-top: 1.5rem;
  padding: 13px;
  transition: all ease-in-out 0.3s;
  background-color: rgba(0,0,0,0.2);
  color: rgba(255,255,255,0.9);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.submit-btn:hover {
  background-color: rgba(0,0,0,0.3);
}

.login-txt {
  margin-top: 1rem;
  font-size: 1rem;
  font-weight:200;
}

.signup-items {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.radio-items {
  display: flex; 
  align-items: center;
}

.form-check {
  width: 5rem;
  display: flex;
  align-items: center;
  gap: 8px;
}


</style>

