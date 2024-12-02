<template>
  <div>
    <div v-if="movie" class="md-container">
      <div
        class="backdrop-container"
        :style="{ backgroundImage: `url(${getImageUrl(movie.backdrop_path)})`}"
        width="100%"
      ></div>

      <div class="left-container">
        <div class="md-poster">
          <img
            class="md-poster-img"
            :src="getImageUrl(movie.poster_path)"
            alt=""
            width="100%"
          />
        </div>
        <button class="like-btn" @click="toggleLike">
          {{ isLiked ? "♥ like cancle" : "♡ like" }}
        </button>
      </div>
      <div class="right-container">
        <div class="top-container">
          <div class="top-inner">
            <div class="movie-title-containter">
              <div class="md-movie-title">{{ movie.title }}</div>
            </div>
            <div class="movie-info">
              <p>
                <b>{{ getReleaseYear(movie.release_date) }}</b>
              </p>
              <p>RUNTIME · {{ movie.runtime }}mins</p>
              <p>TMDB 평점: {{ movie.vote_average }}</p>
            </div>
            <div class="genre-container">
              <div v-for="genre in movie.genres" :key="genre.id" class="genre">
                # {{ genre.name }}
              </div>
            </div>
          </div>
        </div>
        <div class="bottom-container">
          <div id="carouselExampleFade" class="carousel slide">
            <div>
              <div class="line-css"></div>
            </div>
            <div class="carousel-inner">
              <div class="carousel-item active">
                <div class="bottom-inner">
                  <div class="overview-txt">OVERVIEW</div>
                  <div class="bb-container">
                    <div class="movie-overview">{{ movie.overview }}</div>
                    <button
                      type="button"
                      class="youtube-icon-btn"
                      @click="fetchTrailer"
                      data-bs-toggle="modal"
                      data-bs-target="#exampleModal"
                    >
                      <i class="fa-brands fa-youtube youtube-icon"></i>
                    </button>
                    <div v-if="streamingServices.length > 0" class="streaming-container">
                      <div class="provided-txt">Provided in</div>
                      <div v-for="(imgUrl, index) in streamingImgUrl" :key="index" class="streaming-logo">
                        <img
                          :src="getImageUrl(imgUrl)"
                          alt=""
                          width="26px"
                          data-bs-toggle="tooltip"
                          data-bs-placement="top"
                          :data-bs-title="streamingServices[index]"
                          ref="tooltipImage"
                        />
                        <!-- 스트리밍 서비스 로고 이미지 출력 -->
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="carousel-item">
                <div class="bottom-inner">
                  <div class="overview-txt">ARTICLES</div>
                  <div class="article-container">
                    <button class="create-link" @click="goCreateArticle">create</button>
                      <MovieArticleList/>
                    </div>
                </div>
              </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleFade" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div
        class="modal fade"
        id="exampleModal"
        tabindex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">
                {{ movie.title }} 예고편
              </h1>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <iframe
                v-if="trailerUrl"
                :src="trailerUrl"
                width="100%"
                height="315"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
              <p v-else>예고편을 찾을 수 없습니다.</p>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/movie";
import { useCounterStore } from "@/stores/counter";
import {
  RouterLink,
  useRoute,
  RouterView,
  onBeforeRouteUpdate,
  useRouter,
} from "vue-router";
import { onMounted, ref, nextTick } from "vue";
import axios from "axios";
import MovieArticleList from '@/components/MovieArticleList.vue'

const router = useRouter();
const route = useRoute();
const movieStore = useMovieStore();
const counterStore = useCounterStore();
const movieId = ref(route.params.movieId);
const movie = ref(null);
const trailerUrl = ref(null);
const streamingServices = ref([]);
const streamingImgUrl = ref([]);

const isLiked = ref(null); // 현재 사용자가 좋아요한 상태 여부

const fetchLikeStatus = async () => {
  try {
    const response = await axios.get(
      `${counterStore.API_URL}/users/liked-movies/`,
      {
        headers: {
          Authorization: `Token ${counterStore.token}`,
        },
      }
    );
    console.log("좋아요 상태 응답:", response.data); // 응답 로그
    const likedMovies = response.data.liked_movies;
    isLiked.value = likedMovies.includes(movieId.value); // 영화 ID가 포함되어 있는지 확인
    console.log("isLiked:", isLiked.value); // 상태 로그
  } catch (error) {
    console.error("좋아요 상태 확인 오류:", error);
  }
};

const toggleLike = async () => {
  try {
    const response = await axios.post(
      `${counterStore.API_URL}/api/v1/movies/${movieId.value}/like/`,
      {},
      {
        headers: {
          Authorization: `Token ${counterStore.token}`,
        },
      }
    );
    console.log(response.data.message);
    isLiked.value = response.data.liked; // 서버에서 변경된 상태를 반환받아 업데이트
  } catch (error) {
    console.error("좋아요 처리 중 오류:", error);
  }
};

const getImageUrl = (path) => {
  const baseUrl = "https://image.tmdb.org/t/p/";
  const size = "w1280"; // 더 나은 화질을 위해 w1280 또는 original 사용
  return `${baseUrl}${size}${path}`;
};

// YouTube API Key (Replace with your actual key)
const YOUTUBE_API_KEY = movieStore.YOUTUBE_API_KEY;

const goCreateArticle = () => {
  router.push({ name: "CreateView" });
};

//스트리밍 서비스 정보 가져오기
const fetchWatchProviders = async () => {
  const options = {
    method: "GET",
    url: `https://api.themoviedb.org/3/movie/${movieId.value}/watch/providers`,
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${movieStore.TMDB_KEY}`,
    },
  };

  try {
    const response = await axios.request(options);
    const providers = response.data.results?.["KR"]?.flatrate || []; // 한국(KR) 기준 스트리밍 서비스
    streamingServices.value = providers.map(
      (provider) => provider.provider_name
    ); // 서비스 이름만 저장
    streamingImgUrl.value = providers.map((provider) => provider.logo_path);
    console.log("Streaming Services:", streamingServices.value);
  } catch (error) {
    console.error("Watch Providers API 호출 오류:", error);
    streamingServices.value = [];
  }
};

//유튜브 통해서 예고편 가져오기
const fetchTrailer = async () => {
  // 영화 제목과 "official trailer"로 검색 쿼리 생성
  const query = `${movie.value.original_title} official trailer`;
  console.log(movie.value);

  // 검색 API URL: 기본적으로 가장 관련성 높은 결과가 위에 표시됨
  const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${query}&type=video&order=relevance&key=${YOUTUBE_API_KEY}`;

  try {
    const response = await axios.get(url);
    const videoId = response.data.items[0]?.id?.videoId; // 검색 결과 중 첫 번째 영상
    if (videoId) {
      trailerUrl.value = `https://www.youtube.com/embed/${videoId}`;
    } else {
      console.warn("예고편을 찾을 수 없습니다.");
      trailerUrl.value = null;
    }
  } catch (error) {
    console.error("YouTube API 호출 오류:", error);
    trailerUrl.value = null;
  }
};

//movie객체 정보 채우기
const fetchMovieData = () => {
  const options = {
    method: "GET",
    url: `https://api.themoviedb.org/3/movie/${movieId.value}`,
    params: { language: "ko-KR" }, // 언어를 한국어로 설정
    headers: {
      accept: "application/json",
      Authorization: `Bearer ${movieStore.TMDB_KEY}`,
    },
  };
  axios
    .request(options)
    .then((res) => {
      movie.value = res.data;
      movieId.value = res.data.id;
      console.log(res.data);
    })
    .catch((err) => console.error(err));
};

onMounted(async () => {
  await fetchMovieData();
  await fetchLikeStatus(); // 좋아요 상태 가져오기
  await fetchWatchProviders();
  const tooltipTriggers = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );
  tooltipTriggers.forEach((trigger) => {
    new bootstrap.Tooltip(trigger);
  });

  nextTick(() => {
    const modal = document.getElementById("exampleModal");
    if (modal) {
      modal.addEventListener("hidden.bs.modal", () => {
        trailerUrl.value = null; // iframe src 제거
      });
    } else {
      console.error("Modal element not found.");
    }
  });
});

const getReleaseYear = (releaseDate) => {
  return releaseDate.slice(0, 4); // 앞 4글자 (연도)만 가져오기
};

// 디데일 창에서도 영화 검색이 잘되도록 라우트 업데이트
onBeforeRouteUpdate(async (to, from) => {
  movieId.value = to.params.movieId;
  await fetchMovieData(); // 라우트가 업데이트될 때 파라미터 값을 갱신
  await fetchWatchProviders();
  const tooltipTriggers = document.querySelectorAll(
    '[data-bs-toggle="tooltip"]'
  );
  tooltipTriggers.forEach((trigger) => {
    new bootstrap.Tooltip(trigger);
  });
});
</script>

<style scoped>
* {
  font-family: "Noto Sans KR", sans-serif;
}

/* YouTube Button Style - Icon Only */
.youtube-icon-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.youtube-icon {
  font-size: 2rem;
  color: #fe0606; /* YouTube brand color */
}

.backdrop-container {
  z-index: -5;
  position: absolute;
  width: 100%;
  height: 60vw; /* 원하는 높이 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  margin-bottom: 20px;
  filter: blur(7px) brightness(20%);
}

.md-container {
  width: 100%;
  display: flex;
  height: 90vh;
  overflow: hidden;
  padding-top: 2rem;
}

.left-container {
  width: 30%;
  display: flex;
  flex-direction: column;
  /* justify-content: center; */
  padding: 20px 30px;
}

.md-poster-txt {
  font-size: 1.8vw;
  font-weight: 300;
  margin: 0 0 0.7rem 0.5rem;
  opacity: 0.8;
}

.md-poster {
  border-radius: 10px;
  overflow: hidden;
  perspective: 100px;
  box-shadow: 2px 2px 50px rgba(255, 255, 255, 0.1);
}

.right-container {
  width: 70%;
}

.top-container {
  display: flex;
  flex-direction: row-reverse;
  margin-top: 4vw;
}

.top-inner {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.md-movie-title {
  width: 120%;
  letter-spacing: 2px;
  font-size: 3vw;
  padding: 0 1.9vw 1.3vw 0;
}

.movie-info {
  position: relative;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  font-size: 1.2vw;
  opacity: 0.7;
  display: flex;
  gap: 10px;
  font-weight: 300;
  padding: 0.5rem 2vw 0.5rem 5vw;
}

.movie-info::before {
  content: "";
  position: absolute;
  top: -0.2rem;
  left: 0;
  width: 0.3rem;
  height: 0.3rem;
  background-color: gray;
  border-radius: 50%;
}

.genre-container {
  font-size: 1vw;
  display: flex;
  gap: 10px;
  font-weight: 100;
  padding-right: 2vw;
}

.genre {
  padding: 0.3vw 0.8vw;
  border: 1px solid gray;
  border-radius: 15px;
}

.bottom-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  letter-spacing: 1px;
  line-height: 2vw;
  padding: 0 0 0 1vw;
}

.overview-txt {
  font-weight: 200;
  font-size: 1.8vw;
  opacity: 0.8;
  padding-bottom: 0.7vw;
}

.line-css {
  position: absolute;
  z-index: -1;
  top: 3vw;
  left: -10vw;
  width: 23vw;
  height: 1px;
  background-color: gray;
}

.line-css::after {
  content: "";
  position: absolute;
  top: -0.1rem;
  right: 0;
  width: 0.3rem;
  height: 0.3rem;
  background-color: gray;
  border-radius: 50%;
}

.movie-overview {
  font-size: 1.3vw;
  font-weight: 200;
}

.streaming-container {
  display: flex;
  align-items: center;
  gap: 5px;
}

.provided-txt {
  font-size: 1.2vw;
  font-weight: 100;
}

.streaming-logo {
  display: flex;
  align-items: center;
}

.bottom-inner {
  width: 65vw;
  height: 25vw;
}

.carousel-control-prev {
  width: 32px;
  left: -25px;
}

.carousel-control-next {
  width: 32px;
  right: -25px;
}
.bb-container {
  padding: 0 15px;
  padding-top: 1.8vw;
}

.article-container {
  padding: 0 15px;
  padding-top: 1.8vw;
}

.like-btn {
  border: none;
  width: 8rem;
  transition: all ease-in-out 0.3s;
  background-color: rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 0.3rem;
  border-radius: 15px;
  margin-top: 1rem;
}

.like-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);

}

.create-link {
  background-color: rgba(255, 255, 255, 0.2);
  transition: all ease-in-out 0.3s;
  border: none;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.2rem;
  font-weight: 300;
  border-radius: 25px;
  padding: 0.3rem 0.5rem;
  width: 7rem;
  /* height: 2rem; */
}

.create-link:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
