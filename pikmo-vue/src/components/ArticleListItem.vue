<template>
    <div class="article-container" @click="(event) => goDetail(event, article)" >
      <div class="img-container">
        <img v-if="movie?.poster_path"  class="movie-img" :src="getImageUrl(movie.backdrop_path)" alt="" width="100%">
      </div>
      <div class="wrapper">
        <div class="movie-items">
          <div class="movie-title">{{ movie.title }}</div>
          <div class="dot-btn" @click="(event) => goDetail(event, movie)" data-bs-toggle="tooltip" title="Go to movie detail"><div class="dot-btn-txt">···</div></div>
        </div>
        <div class="article-items">
          <div class="article-username"><div class="username">{{ counterStore.getUsername(article.user_id) }}</div></div>
          <div class="article-title">{{ article.title }}</div>
          <div class="article-content">{{ article.content }}</div>
        </div>
      </div>
    </div>
    <div class="black-css"></div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';
import { useCounterStore } from '@/stores/counter';

const props = defineProps({
  article: Object,
});

const movieStore = useMovieStore()
const counterStore = useCounterStore()
const movie = ref({})
const movieId = ref(null)
const router = useRouter()


const username = computed(() => counterStore.username);

const getImageUrl = (path) => {
    const baseUrl = "https://image.tmdb.org/t/p/";
    const size = "w1280"; // 더 나은 화질을 위해 w1280 또는 original 사용
    return `${baseUrl}${size}${path}`;
  }

const goDetail = (event, object) => {
  if(event.target.classList.value === 'dot-btn-txt'){
    // 툴팁 초기화, 화면에서 잘 사라지게끔
    const tooltip = bootstrap.Tooltip.getInstance(event.currentTarget);
    if (tooltip) tooltip.hide();

    event.stopPropagation()
    router.push(`${object.id}`);
  }else{
    router.push({ 
    name: 'ArticleDetailView',
    params: {
      id: object.id,
    } 
    });
  }
}

const fetchMovieData = () => {
    const options = {
      method: 'GET',
      url: `https://api.themoviedb.org/3/movie/${movieId.value}`,
      params: { language: 'ko-KR' },  // 언어를 한국어로 설정
      headers: {
        accept: 'application/json',
        Authorization:  `Bearer ${movieStore.TMDB_KEY}`,
      }
    };
    axios
      .request(options)
      .then(res => {
        movie.value = res.data;
      })
      .catch(err => console.error(err));
  }

onMounted(async () => {
  movieId.value = props.article.movie_id
  const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggers.forEach(trigger => {
    new bootstrap.Tooltip(trigger);
  });
  await fetchMovieData();
})


</script>

<style scoped>
* {font-family: "Noto Sans KR", sans-serif;;}

a {
  text-decoration: none; /* 밑줄 제거 */
  color: inherit; /* 부모 요소의 색상 상속 */
  background: none; /* 배경 제거 */
  outline: none; /* 포커스 시 아웃라인 제거 */
}

.article-container {
  position: relative;
  width: 27rem;
  border-radius: 15px;
  transition: all 0.3s ease-in-out;
  overflow: hidden;
  background-color: none;
}

.img-container {
  overflow: hidden;
  transition: all 0.3s ease-in-out;
  filter: blur(1px) grayscale(100%) brightness(60%);
}

.article-container:hover .img-container {
  filter: grayscale(0%) brightness(90%); /* 색상 돌아오기 */
}

.article-container:hover {
  transform: translateY(-10px); /* 이미지 살짝 올라가게 */
}

.wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 0;
  color: white;
}

.movie-items {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 1rem 1rem 5rem 0;
}

.movie-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-right: 0.5rem;
}

.dot-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  transition: all 0.3s ease-in-out;
  background-color: rgba(220,220,220,0.3);
  overflow: hidden;
}

.dot-btn:hover {
  background-color: rgba(200, 200, 200, 0.2);
}

.dot-btn-txt {
  font-size: 0.8rem;
  font-weight: 700;
}

.article-items {
  display: flex;
  flex-direction: column;
  padding: 0 0 0 1rem;
  flex: 1;
  gap: 0.5rem;
}

.article-username {
  background-color: rgba(220,220,220,0.3);
  transition: all 0.3s ease-in-out;
  width: 5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 15px;
}

.article-username:hover {
  background-color: rgba(200, 200, 200, 0.2);
}

.article-title {
  font-size: 1.2rem;
  padding-left: 0.5rem;
  font-weight: 400;
  width: 22rem;
  display: -webkit-box;           /* 플렉스 기반 레이아웃 */
  -webkit-line-clamp: 1;          /* 최대 줄 수 설정 (여기선 3줄) */
  -webkit-box-orient: vertical;   /* 수직 박스 방향 지정 */
  overflow: hidden;
}

.article-content {
  font-size: 0.9rem;
  padding: 0 0.5rem;
  font-weight: 300;
  display: -webkit-box;           /* 플렉스 기반 레이아웃 */
  -webkit-line-clamp: 1;          /* 최대 줄 수 설정 (여기선 3줄) */
  -webkit-box-orient: vertical;   /* 수직 박스 방향 지정 */
  overflow: hidden;
}

</style>