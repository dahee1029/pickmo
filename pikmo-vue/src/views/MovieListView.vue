<template>
  <div>
    <div id="carouselExample" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <!-- 반복문을 돌면서 첫 번째 항목에 'active' 클래스 추가 -->
        <div
          v-for="(movie, index) in store.movies2"
          :key="movie.id"
          class="carousel-item"
          :class="{ active: index === 0 }"
          data-bs-interval="4000"
        >
          <div
            class="d-flex justify-content-center align-items-center w-100 position-relative"
          >
            <div class="c-movie-gradient"></div>
            <div class="c-movie-content">
              <div class="c-movie-title">{{ movie.title }}</div>
              <div class="c-movie-overview">{{ movie.overview }}</div>
              <div
                class="more-btn"
                @click="(event) => goDetail(event, movie, 'main')"
              >
                <div>
                  More info
                </div>
              </div>
            </div>
            <img
              :src="getImageUrl(movie.backdrop_path)"
              class="c-movie-img"
              alt="..."
            />
          </div>
        </div>
      </div>
      <button class="carousel-control-prev">
        <span
          class="carousel-control-prev-icon"
          type="button"
          data-bs-target="#carouselExample"
          data-bs-slide="prev"
          aria-hidden="true"
        ></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <div class="carousel-control-next">
        <span
          class="carousel-control-next-icon"
          type="button"
          data-bs-target="#carouselExample"
          aria-hidden="true"
          data-bs-slide="next"
        ></span>
        <span class="visually-hidden">Next</span>
      </div>
    </div>
    <div class="carousel-container">
      <div class="c3-title">POPULAR MOVIES</div>
      <carousel-3d :height="500">
        <slide
          v-for="(movie, i) in store.movies"
          :index="i"
          :key="movie.id"
          v-slot="{ index, isCurrent, leftIndex, rightIndex }"
          :style="{ border: 'none' }"
        >
          <img
            :data-index="index"
            :class="{
              current: isCurrent,
              onLeft: leftIndex >= 0,
              onRight: rightIndex >= 0,
            }"
            :src="getImageUrl(movie.poster_path)"
            @click="(event) => goDetail(event, movie, 'carousel')"
          />
        </slide>
      </carousel-3d>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/movie";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Carousel3d, Slide } from "vue3-carousel-3d";

const store = useMovieStore();
const router = useRouter();

// Navigate to movie details
const goDetail = (event, movie, where) => {
  if (event.target.classList.value === "current") {
    router.push(`${movie.id}`);
  } else if (where === "main") {
    router.push(`${movie.id}`);
  }
};

// Add the base URL to poster_path
const getImageUrl = (path) => {
  const baseUrl = "https://image.tmdb.org/t/p/";
  const size = "w1280"; // 더 나은 화질을 위해 w1280 또는 original 사용
  return `${baseUrl}${size}${path}`;
};
const movies1 = ref([]);

// Fetch movies on mount
onMounted(async () => {
  // store.getMovies("top_rated");
  store.getMovies("now_playing");
});
</script>

<style scoped>
/* font-family: "Noto Sans KR", sans-serif; */
* {
  font-family: "Noto Sans KR", sans-serif;
}

.carousel-container {
  padding: 30px 0;
}

img:not(.c-movie-img) {
  width: 100%;
  height: auto;
  filter: brightness(30%);
}

img.current {
  filter: brightness(100%);
}

.c-movie-gradient {
  position: absolute;
  left: 0;
  width: 80%;
  height: 100%;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 1),
    rgba(0, 0, 0, 0.8) 50%,
    rgba(0, 0, 0, 0) 100%
  );
  z-index: -1;
}

.c-movie-content {
  /* position: absolute; */
  left: 10%;
  z-index: 0;
  color: white;
  font-size: 15px;
  padding: 0 60px;
  width: 35%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.c-movie-img {
  width: 65%;
  z-index: -2;
}

.c-movie-title {
  font-weight: 700;
  font-size: 3vw;
  margin: 20px 0;
  width: 200%;
}

.c-movie-overview {
  display: -webkit-box; /* 플렉스 기반 레이아웃 */
  -webkit-line-clamp: 3; /* 최대 줄 수 설정 (여기선 3줄) */
  -webkit-box-orient: vertical; /* 수직 박스 방향 지정 */
  overflow: hidden; /* 넘치는 텍스트 숨김 */
  width: 170%;
  font-size: 1.4vw;
  margin-bottom: 20px;
  line-height: 1.4;
}

.c-movie-btn {
  width: 12vw;
  max-width: 200px;
  font-size: 1.2vw;
}

.carousel-control-prev {
  height: 32px;
  width: 50px;
  margin: auto 0;
  display: block;
}

.carousel-control-next {
  height: 32px;
  width: 50px;
  margin: auto 0;
  display: block;
}

.carousel-container {
  display: flex;
  flex-direction: column;
  padding: 0 40px;
}

.c3-title {
  font-weight: 200;
  font-size: 2.5vw;
  margin: 10px 0;
}

.more-btn {
  width: 7rem;
  transition: all ease-in-out 0.3s;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.6rem;
  font-size: 1rem;
  border-radius: 15px;
  font-weight: 300;
}

.more-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
