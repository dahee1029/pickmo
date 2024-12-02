<template>
  <div>
    <div class="background-img">
      <img src="https://image.tmdb.org/t/p/original/6ASfLUVXRyXct9xlyExpuXIDULX.jpg" alt="" width="100%">
    </div>
    <div class="p-container">
      <div class="p-header">
        <div class="likes-txt">likes</div>
      </div>
      <div class="p-inner">
        <div v-if="likedMovies.length > 0" class="liked-list">
          <div v-for="movie in likedMovies" :key="movie.id" class="liked-movie" width="250px">
            <img v-if="movie.title" :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="영화 포스터" width="250px" @click="goDetail(movie)"/>
          </div>
        </div>
        <div v-else>
          <p>Nothings Here.</p>
        </div>
      </div>
    </div>
    <div class="profile-container" v-if="user">
      <div class="profile-inner">
        <div class="username">{{ user.username }}</div>
        <div class="genre-wrapper">
          <div class="like-genre" v-if="user.favorite_genres && user.favorite_genres.length > 0">
            # {{ user.favorite_genres.join(", ") }}
          </div>
          <div class="like-genre" v-else># All</div>
        </div>
        <div class="user-info-list">
          <div class="user-info"><div class="field-name">gender</div> {{ user.gender === "f" ? "female" : "male" }}</div>
          <div class="user-info"><div class="field-name">email</div>  {{ user.email }}</div>
        </div>
      </div>
      <div class="profile-update" @click="updateProfile">
        UPDATE
      </div>
    </div>
  </div>






  <div>
    <h1>프로필 페이지</h1>
    <div v-if="user">
      <p><strong>유저명:</strong> {{ user.username }}</p>
      <p><strong>성별:</strong> {{ user.gender === "f" ? "여성" : "남성" }}</p>
      <p><strong>이메일:</strong> {{ user.email }}</p>
      <p>
        <strong>좋아하는 장르:</strong>
        <span v-if="user.favorite_genres && user.favorite_genres.length > 0">
          {{ user.favorite_genres.join(", ") }}
        </span>
        <span v-else>선택한 장르 없음</span>
      </p>

      <div>
        <h3>좋아하는 영화</h3>
        <div v-if="likedMovies.length > 0">
          <ul>
            <li v-for="movie in likedMovies" :key="movie.id">
              <h4 v-if="movie.title">{{ movie.title }}</h4>
              <img v-if="movie.title" :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="영화 포스터" />
            </li>
          </ul>
        </div>
        <div v-else>
          <p>좋아하는 영화가 없습니다.</p>
        </div>
      </div>

      <button @click="updateProfile">프로필 수정</button>
    </div>
    <div v-else>
      <p>로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";

const user = ref(null);
const likedMovies = ref([]);  // 좋아하는 영화 리스트
const counterStore = useCounterStore();
const API_URL = counterStore.API_URL;
const route = useRoute();
const user_pk = route.params.user_pk;
const router = useRouter();
const token = counterStore.token;


const goDetail = async (movie) => {
  await router.push({
    name: "movie_detail",
    params: {
      movieId: movie.id,
    },
  });
};
// 프로필 수정 페이지로 이동
const updateProfile = () => {
  router.push({ name: "UpdateProfileView", params: { user_pk: user_pk } });
};

// 좋아하는 영화 가져오기
const getLikedMovies = () => {
  axios({
    method: "get",
    url: `${API_URL}/users/liked-movies/`,
    headers: {
      Authorization: `Token ${token}`,
    },
  })
    .then((res) => {
      likedMovies.value = res.data.liked_movies;  // 영화 ID 리스트
      console.log(likedMovies.value)
      getMovieDetails(res.data.liked_movies);  // 영화 상세 정보 가져오기
    })
    .catch((err) => {
      console.log(err);
    });
};

// 영화 상세 정보 가져오기
const getMovieDetails = (movieIds) => {
  movieIds.forEach((movieId) => {
    axios({
      method: "get",
      url: `https://api.themoviedb.org/3/movie/${movieId}`,
      params: { language: "ko-KR" },
      headers: {
        accept: "application/json",
        Authorization: `Bearer ${counterStore.TMDB_KEY}`,
      },
    })
      .then((res) => {
        // 영화 정보를 likedMovies 배열에 추가
        likedMovies.value.push(res.data);
      })
      .catch((err) => {
        console.error("영화 정보를 불러오는 중 오류 발생:", err);
      });
  });
};

onMounted(() => {
  if (!counterStore.token) {
    console.error("유효한 인증 토큰이 없습니다.");
    return;
  }
  if (!user_pk) {
    console.error("user_pk가 유효하지 않습니다.");
    return;
  }
  
  // 유저 정보 가져오기
  axios({
    method: "get",
    url: `${API_URL}/users/profile/${user_pk}/`,
    headers: {
      Authorization: `Token ${counterStore.token}`,
    },
  })
    .then((response) => {
      user.value = response.data;
      console.log(user.value);
    })
    .catch((error) => {
      console.error("유저 정보를 불러오는 중 오류 발생:", error);
    });

  // 좋아하는 영화 정보 가져오기
  getLikedMovies();
});
</script>

<style scoped>
* {font-family: "Noto Sans KR", sans-serif;}

.background-img {
  height: 22rem;
  position: relative;
  /* overflow: hidden; */
}

.p-container {
  height: 100vw;
  background-color: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(50px);
}

.p-header {
  height: 4rem;
  background-color: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
}

.likes-txt {
  margin-left: 30rem;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.7);
}

.p-inner {
  margin: 1.2rem 0 0 30rem;
}

.liked-list {
  display: flex;
  /* gap: 1rem; */
  flex-wrap: nowrap;
  max-width: 82rem;
  overflow-x: auto;
}

.liked-movie > img {
  height: 22rem;
  border-radius: 10px;
  margin-right: 1rem;
}

.profile-container {
  position: absolute;
  top: 17rem;
  left: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.profile-update{
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(50px);
  border-radius: 18px;
  font-size: 1.2rem;
  transition: all ease-in-out 0.3s;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 300;
  text-align: center;
}

.profile-update:hover {
  background-color: rgba(255, 255, 255, 0.3);
}


.profile-inner {
  width: 25rem;
  height: 21rem;
  background-color: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(50px);
  border-radius: 25px;

  display: flex;
  flex-direction: column;
  padding: 2rem;
}

.username {
  font-size: 3rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  padding-bottom: 1.2rem;
  border-bottom: 2px dashed rgba(255, 255, 255, 0.3);
}

.user-info-list {
  display: flex;
  flex-direction: column;
  margin-top: 4rem;
}

.user-info {
  padding: 0.8rem 1rem;
  display: flex;
  font-size: 1.1rem;
  /* background-color: rgba(0, 0, 0, 0.3); */
  margin-bottom: 0.3rem;
  border-radius: 25px;
}

.field-name {
  width: 4.5rem;
}

.genre-wrapper {
  margin-top: 0.5rem;
  display: flex;
  flex-direction: row-reverse;
}

.like-genre {
  padding: 0.3rem 0.7rem;
  border-radius: 15px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.5);
  border: 1px solid;
}



</style>
