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
      <div class="update-txt">Change Password</div>
      <div class="update-items">
        <form @submit.prevent="submitPasswordChange" class="update-form">
          <label class="c-password-label" for="current_password">Current Password</label>
          <input class="c-password-input" type="password" id="current_password" v-model="passwords.current" placeholder="Enter your current password." required/><br>

          <input class="new-password-input" type="password" id="new_password" v-model="passwords.new" placeholder="Enter your new password."><br>
          <input class="new-password-input" type="password" id="confirm_password" v-model="passwords.confirm" placeholder="Please re-enter your password."><br>

          <input class="submit-btn" type="submit" value="Update">
        </form>
      </div>
    </div> 
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";

const passwords = ref({
  current: "",
  new: "",
  confirm: "",
});

const counterStore = useCounterStore();
const API_URL = counterStore.API_URL;
const user_pk = useRoute().params.user_pk;
const router = useRouter();

const submitPasswordChange = async () => {
  if (passwords.value.new !== passwords.value.confirm) {
    alert("새 비밀번호와 확인 비밀번호가 일치하지 않습니다.");
    return;
  }

  try {
    const response = await axios.put(
      `${API_URL}/users/profile/change-password/`,
      {
        current_password: passwords.value.current,
        new_password: passwords.value.new,
        confirm_password: passwords.value.confirm,
      },
      {
        headers: {
          Authorization: `Token ${counterStore.token}`,
        },
      }
    );

    alert(response.data.message || "비밀번호가 성공적으로 변경되었습니다.");
    passwords.value = { current: "", new: "", confirm: "" };
    router.push({ name: "UpdateProfileView", params: { user_pk } });
  } catch (error) {
    console.error("비밀번호 변경 중 오류 발생:", error);
    alert(error.response?.data?.error || "비밀번호 변경에 실패했습니다.");
  }
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
  height: 28rem;
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

.update-txt {
  /* margin-top: 1rem; */
  font-size: 2rem;
}

.update-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.c-password-input, .new-password-input {
  all: unset;
  padding: 10px 5px;
  border: none;
  border-bottom: 2px solid rgba(255,255,255,0.9);
  background: none;
  letter-spacing: 1px;
  font-weight:200;
}

.c-password-label {
  margin: 1.5rem 0 0 0;
}

.c-password-input::placeholder, .new-password-input::placeholder{
  color: rgba(255,255,255,0.9);
}

.c-password-input:focus, .new-password-input:focus {
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

.update-items {
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

