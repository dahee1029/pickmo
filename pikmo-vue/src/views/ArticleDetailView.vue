<template>
  <div>
    <div
      v-if="movie?.backdrop_path"
      class="background-img"
      :style="{ backgroundImage: `url(${getImageUrl(movie.backdrop_path)})` }"
    >
      <div class="ad-container">
        <div class="left-blur"></div>
        <div class="movie-container">
          <div class="movie-t-wrapper">
            <div class="movie-title">{{ movie.title }}</div>
            <div class="movie-info">
              <p>
                <b>{{ getReleaseYear(movie.release_date) }}</b>
              </p>
              <p>RUNTIME · {{ movie.runtime }}mins</p>
              <p>TMDB 평점: {{ movie.vote_average }}</p>
            </div>
          </div>
          <div class="movie-b-wrapper">
            <div class="movie-overview">{{ movie.overview }}</div>
            <div class="movie-btn" @click="goMovieDetail">
              <div>LINK TO MOVIE</div>
            </div>
          </div>
        </div>
        <div class="article-container">
          <div v-if="article" class="article-inner">
            <div class="article-header">
              <div class="article-id">
                {{ getArticleId(article.id) }} ARTICLE
              </div>
              <div class="article-username">
                {{ store.getUsername(article.user) }}
              </div>
            </div>
            <div class="article-title">{{ article.title }}</div>
            <div class="article-content">{{ article.content }}</div>
            <!-- <p>작성일 : {{ formatDate(article.created_at) }}</p> -->
            <!-- <p>수정일 : {{ formatDate(article.updated_at) }}</p> -->
          </div>
          <div class="comment-container">
            <div class="comment-header">
              <div class="comment-txt"><div>COMMENT</div></div>
            </div>
            <div v-if="comments && comments.length > 0" class="comment-list">
              <div
                v-for="comment in comments"
                :key="comment.id"
                class="comment-wrapper"
              >
                <div class="comment-items">
                  <div class="comment-username">{{ comment.username }}</div>
                  |
                  <div class="comment-content">{{ comment.content }}</div>
                </div>
                <div
                  class="btn-close"
                  v-if="comment.username === username"
                  @click="deleteComment(comment.id)"
                ></div>
              </div>
            </div>
            <!-- <div v-else>
              <p>No comments yet.</p>
            </div> -->
            <form @submit.prevent="submitComment" class="comment-form">
              <input
                v-model="newComment"
                placeholder="Type you comment"
                required
                class="comment-input"
              />
              <button type="submit" class="comment-btn"><div>SEND</div></button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref, computed } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute, useRouter } from "vue-router";
import dayjs from "dayjs";
const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);
const comments = ref([]);
const newComment = ref("");

const article_pk = route.params.id;
const username = computed(() => store.username);

// 게시글 영화 관련 정보 가져오기
import { useMovieStore } from "@/stores/movie";
import { watch } from "vue";
const movieStore = useMovieStore();
const movie = ref({});
const movieId = ref(null);

watch(
  () => movieId.value,
  (newMovieId) => {
    if (newMovieId) {
      fetchMovieData();
    }
  }
);

const getImageUrl = (path) => {
  const baseUrl = "https://image.tmdb.org/t/p/";
  const size = "w1280"; // 더 나은 화질을 위해 w1280 또는 original 사용
  return `${baseUrl}${size}${path}`;
};

const goMovieDetail = () => {
  router.push({
    name: "movie_detail",
    params: { movieId: article.value.movie_id },
  });
};

const getReleaseYear = (releaseDate) => {
  return releaseDate.slice(0, 4); // 앞 4글자 (연도)만 가져오기
};

const getArticleId = (id) => {
  if (id < 10) {
    return `0${id}`;
  } else {
    return id;
  }
};

// DRF로 전체 댓글 요청을 보내고 응답을 받아 comments에 저장하는 함수
const getComments = function () {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${article_pk}/comments`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      comments.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

// dayjs로 날짜 포맷을 '2024년 11월 21일' 형식으로 변경
const formatDate = (dateStr) => {
  return dayjs(dateStr).format("YYYY년 MM월 DD일");
};

// 댓글 생성 함수
const submitComment = function () {
  if (newComment.value.trim() === "") return;

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/${article_pk}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      content: newComment.value,
    },
  })
    .then((res) => {
      comments.value.push(res.data); // 새로운 댓글을 댓글 목록에 추가
      newComment.value = ""; // 댓글 작성 후 입력창 초기화
    })
    .catch((err) => {
      console.log(err);
    });
};

// 댓글 삭제 함수
const deleteComment = function (commentId) {
  axios({
    method: "delete",
    url: `${store.API_URL}/api/v1/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then(() => {
      // 삭제 성공 시, 댓글 목록에서 해당 댓글을 제거
      comments.value = comments.value.filter(
        (comment) => comment.id !== commentId
      );
    })
    .catch((err) => {
      console.log(err);
    });
};

const getArticle = () => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/articles/${article_pk}/`,
  })
    .then((res) => {
      article.value = res.data;
      movieId.value = article.value.movie_id;
    })
    .catch((err) => {
      console.log(err);
    });
};

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
    })
    .catch((err) => console.error(err));
};

// DetailView가 마운트되기 전에 DRF로 단일 게시글 조회를 요청 후 응답 데이터를 저장
onMounted(async () => {
  await getArticle();
  // 게시글 조회 후 댓글 가져오기
  await getComments();
});
</script>

<style scoped>
* {
  font-family: "Noto Sans KR", sans-serif;
}

button {
  all: unset; /* 기본 스타일 모두 제거 */
}

.background-img {
  width: 100%;
  height: 100vh;
  z-index: -10;
  background-size: cover;
  filter: brightness(90%);
}

.ad-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-wrap: wrap;
  position: relative;
}

.left-blur {
  flex: 1;
  max-width: 15rem;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
}

.movie-container {
  width: 30rem;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 1rem;
  /* backdrop-filter: brightness(90%); */
}

.movie-t-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.movie-title {
  font-size: 2.5rem;
  font-weight: 600;
}

.movie-info {
  margin-top: 0.5rem;
  display: flex;
  gap: 3px;
}
.movie-b-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.movie-overview {
  width: 18rem;
  display: -webkit-box; /* 플렉스 기반 레이아웃 */
  -webkit-line-clamp: 4; /* 최대 줄 수 설정 (여기선 3줄) */
  -webkit-box-orient: vertical; /* 수직 박스 방향 지정 */
  overflow: hidden;
  line-height: 1.3rem;
  font-size: 1.1rem;
  opacity: 0.8;
}

.movie-btn {
  margin-top: 1rem;
  transition: all 0.3s ease-in-out;
  background-color: rgba(255, 255, 255, 0.3);
  padding: 0.9rem 1.8rem;
  border-radius: 25px;
}

.movie-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.article-container {
  flex-grow: 1;
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(15px);
  padding: 2rem;
  display: flex;
  /* min-width: 40rem; */
  flex-direction: column;
  padding-bottom: 10rem;
}

.article-inner {
  display: flex;
  /* height: 100%; */
  max-width: 60rem;
  flex-direction: column;
}

.article-title {
  font-size: 1.5rem;
  font-weight: 300;
  padding: 0.8rem 1rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.article-id {
  font-size: 4rem;
  font-weight: 1000;
}

.article-content {
  /* flex: 1; */
  margin-top: 1rem;
  font-size: 1.2rem;
  line-height: 1.4rem;
  letter-spacing: 1px;
  font-weight: 300;
  height: 20rem;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.8rem 1rem;
  border-radius: 15px;
  color: rgba(255, 255, 255, 0.9);
  /* border: 1px solid rgba(255,255,255,0.3); */
}

.article-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.article-username {
  color: rgba(255, 255, 255, 1);
  font-size: 1rem;
  font-weight: 200;
  background-color: rgba(0, 0, 0, 0.2);
  transition: all ease-in-out 0.3s;
  padding: 0.5rem 0.7rem;
  border-radius: 15px;
}

.article-username:hover {
  background-color: rgba(0, 0, 0, 0.4);
}
.comment-container {
  display: flex;
  flex-direction: column;
  max-width: 60rem;
}
.comment-header {
  display: flex;
  justify-content: flex-end;
}

.comment-txt {
  display: flex;
  justify-content: flex-end;
  font-size: 1.7rem;
  margin-top: 1rem;
  padding-bottom: 0.5rem;
  width: 18rem;
  /* border-bottom: 2px solid rgba(255,255,255,0.2); */
}

.comment-form {
  display: flex;
}

.comment-input {
  flex: 1;
  background: none;
  border: none;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 0.7rem 1rem;
  /* margin-right: 1rem; */
  /* border: 2px solid rgba(255,255,255,0.4); */
  border-right: none;
  border-radius: 15px 0 0 15px;
  color: rgba(255, 255, 255, 0.6);
}

.comment-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.comment-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0 15px 15px 0;
  transition: all ease-in-out 0.3s;
  background-color: rgba(0, 0, 0, 0.2);
  color: rgba(255, 255, 255, 0.8);
  /* border: 2px solid rgba(255,255,255,0.4); */
  font-weight: 400;
}

.comment-btn:hover {
  background-color: rgba(255, 255, 255, 0.4);
  color: rgba(0, 0, 0, 0.5);
}

.comment-list {
  display: flex;
  flex-direction: column;
}

.comment-wrapper {
  padding: 0.4rem 0.6rem;
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.2rem;
  border-radius: 15px;
  align-items: center;
  transition: all ease-in-out 0.3s;
}

.comment-wrapper:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.comment-items {
  display: flex;
}

.comment-username {
  font-weight: 500;
  padding-right: 0.5rem;
}

.comment-content {
  padding-left: 0.5rem;
}
</style>
