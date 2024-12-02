<template>
  <div class="l-container">
    <!-- Background Carousel -->
    <div class="background-img">
      <img src="https://image.tmdb.org/t/p/original/6ASfLUVXRyXct9xlyExpuXIDULX.jpg" alt="" width="100%">
    </div>

    <!-- Wrapper with form and backdrop filter -->
    <div class="wrapper">
      <div class="edit-txt">Profile Edit</div>
      <div class="edit-items" v-if="user">
        <form @submit.prevent="submitProfileUpdate" class="edit-form">
          <input class="username-input" type="text" id="username" v-model="user.username" required placeholder="Enter your username to edit."><br>
          <input class="email-input" type="email" id="email" v-model="user.email" required placeholder="Enter your email."><br>
          <div class="genre-wrapper">
            <div class="genre-txt">select genre</div>
            <select class="form-select" aria-label="Default select example" v-model="selectedGenres" multiple>
              <option v-for="genre in genres" :key="genre.id" :value="genre.name">
                {{ genre.name }}
              </option>
            </select>
          </div>
          <div class="ridio-items d-flex mb-3">
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="f" v-model="user.gender" required>
              <label class="form-check-label" for="inlineRadio1">Female</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="m" v-model="user.gender" required>
              <label class="form-check-label" for="inlineRadio2">Male</label>
            </div>
          </div>
          <input class="submit-btn" type="submit" value="Edit">
        </form>
        <div class="login-txt mt-3">Want to change your password?<a href="#" @click="goUpdatePassword">Link.</a></div>
      </div>
    </div> 
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";

const user = ref(null); // 사용자 정보
const counterStore = useCounterStore();
const API_URL = counterStore.API_URL;
const route = useRoute();
const user_pk = route.params.user_pk;
const router = useRouter();
const genres = ref([]); // 장르 목록 초기화
const selectedGenres = ref([]); // 선택된 장르
const isMaxSelected = ref(false);

// 비밀번호 변경 페이지로 이동
const goUpdatePassword = () => {
  router.push({ name: "UpdatePasswordView", params: { user_pk } });
};

// 프로필 정보 수정 함수
const submitProfileUpdate = () => {
  // 유효성 검증 (예: 선택된 장르가 1~3개인지 확인)
  if (selectedGenres.value.length === 0 || selectedGenres.value.length > 3) {
    console.error("선호 장르는 1개 이상 3개 이하로 선택해야 합니다.");
    return;
  }

  axios({
    method: "put",
    url: `${API_URL}/users/profile/${user_pk}/`,
    data: {
      username: user.value.username.trim(), // 공백 제거
      email: user.value.email.trim(), // 공백 제거
      gender: user.value.gender,
      favorite_genres: selectedGenres.value, // 선택된 장르 전송
    },
    headers: {
      Authorization: `Token ${counterStore.token}`,
    },
  })
    .then((response) => {
      console.log("프로필이 수정되었습니다:", response.data);
      router.push({ name: "UserProfileView", params: { user_pk } }); // 수정 완료 후 프로필 페이지로 이동
    })
    .catch((error) => {
      // 오류 처리
      if (error.response) {
        console.error("서버 오류:", error.response.data);
      } else {
        console.error("요청 실패:", error.message);
      }
    });
};
// 장르 목록 가져오기
const getGenres = () => {
  axios({
    method: "get",
    url: `${API_URL}/api/v1/movies/genres/`,
    headers: {
      Authorization: `Token ${counterStore.token}`,
    },
  })
    .then((response) => {
      genres.value = response.data;
    })
    .catch((error) => {
      console.error("장르 목록 불러오기 중 오류 발생:", error);
    });
};

// watch로 selectedGenres를 감시
watch(selectedGenres, (newVal, oldVal) => {
  if (newVal.length > 3) {
    selectedGenres.value = oldVal; // 마지막 선택 제거
    isMaxSelected.value = true;
  } else {
    isMaxSelected.value = false;
  }
});

// 프로필 정보 및 장르 목록 불러오기
onMounted(() => {
  axios({
    method: "get",
    url: `${API_URL}/users/profile/${user_pk}/`,
    headers: {
      Authorization: `Token ${counterStore.token}`,
    },
  })
    .then((response) => {
      user.value = response.data;
      selectedGenres.value = response.data.favorite_genres || []; // 초기 선택값 설정
    })
    .catch((error) => {
      console.error("유저 정보를 불러오는 중 오류 발생:", error);
    });

  getGenres(); // 장르 목록 불러오기
});
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
  height: 37rem;
  padding: 2.5rem;
  background-color: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(50px); /* 배경을 흐리게 처리 */
  border-radius: 15px;
  z-index: 1; /* wrapper가 배경 위에 보이도록 설정 */
  margin: auto; /* 화면 가운데에 배치 */
  top: 45%;
  transform: translateY(-50%);
  gap:10px
}

.edit-txt {
  /* margin-top: 1rem; */
  font-size: 2rem;
}

.edit-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.username-input, .email-input {
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

.username-input::placeholder, .email-input::placeholder{
  color: rgba(255,255,255,0.9);
}

.username-input:focus, .email-input:focus {
  outline: none;
}

.submit-btn {
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

.signup-txt {
  margin-top: 1rem;
  font-size: 1rem;
  font-weight:200;
}

.edit-items {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}


.form-check {
  width: 5rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* .form-select {
  width: 12rem;
} */

.genre-wrapper {
  display: flex;
  /* align-items: center; */
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.genre-txt {
  width: 10rem;
  font-size: 1.1rem;
  font-weight: 300;
}

</style>
