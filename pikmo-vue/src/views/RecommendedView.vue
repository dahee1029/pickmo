<template>
  <div class="container">
    <div class="txt-wrapper">
      <div class="txt-lg-1">당신의 휴식을 위해 <span class="txt-lg-2">찾고 싶은 영화</span></div>
      <div class="txt-sm">분류 별로 원하는 항목 선택에 따라, 자동으로 원하는 영화를 찾아 보여줍니다.</div>
    </div>
    <div class="wrapper">
    <div class="left-container">
      <!-- 장르 선택 -->
      <div class="form-group select-list">
        <div class="select-tag">
          <select v-model="selectedGenre" class="dropdown select-genre">
            <option disabled value="">다음 중 하나를 선택하세요</option>
            <option v-for="genre in genres" :key="genre.id">
              {{ genre.name }}
            </option>
          </select>
        </div>
        <div>장르 중</div>
      </div>

      <!-- 스트리밍 서비스 선택 -->
      <div class="form-group select-list">
        <div class="select-tag">
        <select v-model="selectedStream" class="dropdown select-ott">
          <option disabled value="">다음 중 하나를 선택하세요</option>
          <option v-for="stream in streamservices" :key="stream.provider_id">
            {{ stream.provider_name }}
          </option>
        </select>
      </div>
        <div> OOT 서비스에 있는</div>
      </div>

      <div class="txt-last">영화를 찾을래요!</div>

      <input type="button" value="새로 영화 탐색" class="new-btn">
    </div>

    <div class="right-container">
    <!-- 추천 영화 리스트 -->
      <div v-if="recommendedMovies.length" class="movies-list">
          <div v-for="movie in recommendedMovies" :key="movie.id" class="movie-card">
            <div class="movie-img">
              <img :src="getImageUrl(movie.poster_path)" alt="movie" @click="goDetail(movie)"/>
            </div>
            <!-- <div class="movie-info">
              <strong>{{ movie.title }}</strong>
              <p>평점: {{ movie.vote_average }}</p>
            </div> -->
          </div>
      </div>
      <div v-else-if="selectedGenre && selectedStream" class="loading">
        <p>추천 영화를 가져오는 중...</p>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { useRouter } from 'vue-router';

const selectedGenre = ref(null);
const selectedStream = ref(null);
const recommendedMovies = ref([]);
const store = useMovieStore();
const router=useRouter()
// 반응형 데이터 설정
const genres = computed(() => store.genres);
const streamservices = computed(() => store.streamServices);

const goDetail = async (movie) => {
  await router.push({
    name: "movie_detail",
    params: {
      movieId: movie.id,
    },
  });
};



onMounted(() => {
  store.getGenres();
  store.getStreams();
});

// Add the base URL to poster_path
const getImageUrl = (posterPath) => {
  return posterPath ? `https://image.tmdb.org/t/p/w500${posterPath}` : '/placeholder.jpg';
};

// 선택 변경 시 영화 추천 데이터 가져오기
watch([selectedGenre, selectedStream], async ([genreName, streamName]) => {
  if (genreName && streamName) {
    // 장르 ID 필터링
    const genre = genres.value.find((g) => g.name === genreName);
    const genreId = genre ? genre.id : null;

    // 스트리밍 서비스 ID 필터링
    const stream = streamservices.value.find((s) => s.provider_name === streamName);
    const streamId = stream ? stream.provider_id : null;

    if (genreId && streamId) {
      const options = {
        method: 'GET',
        url: 'https://api.themoviedb.org/3/discover/movie',
        params: {
          language: 'ko-kr',
          with_genres: genreId,
          with_watch_providers: streamId,
          watch_region: 'KR',
          sort_by: 'popularity.desc',
        },
        headers: {
          accept: 'application/json',
          Authorization: `Bearer ${store.TMDB_KEY}`,
        },
      };

      try {
        const response = await axios.request(options);
        recommendedMovies.value = response.data.results || [];
      } catch (error) {
        console.error('Failed to fetch recommended movies:', error);
      }
    } else {
      console.warn('Invalid genre or stream selection.');
      recommendedMovies.value = [];
    }
  } else {
    recommendedMovies.value = [];
  }
});
</script>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
  padding: 70px 0;
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 200;
  font-style: normal;
}

.txt-wrapper {
  margin-bottom: 80px;
}

.txt-lg-1 {
  font-weight: 300;
  font-size: 35px;
  padding: 15px 0;
}
.txt-lg-2 {
  font-weight: 500;
  font-size: 35px;
  padding: 15px 0;
}

.txt-sm {
  font-size: 15px;
}

/* 전체 컨테이너 */
.wrapper {
  display: flex;
  height: 600px;
}
.select-list {
  display: flex;
  align-items: center;
}

.left-container {
  margin-right: 100px;
  font-size: 20px;
}

.select-tag {
  border-bottom: 1px solid white;
}

select {
  font-size: 25px;
  font-weight: 600;
  background-color: black; /* 배경 검정색 */
  color: orange; /* 글자 흰색 */
  border: none; /* 테두리 제거 */
  padding: 10px;
  width: 220px;
  border-radius: 5px;
  appearance: none; /* 기본 브라우저 스타일 제거 */
  -webkit-appearance: none;
  -moz-appearance: none;
 }

 .select-genre {
   width: 140px;
   color: #f1faee;
  }
  .select-ott {
   color: #a8dadc;
 }

select option {
  background-color: gray; /* 옵션 박스 배경 회색 */
  color: black; /* 옵션 글자 검정색 */
}

.txt-last {
  padding:10px;
  margin-bottom: 70px;
}

.new-btn {
  border: none;
  padding: 20px 50px;
  font-size: 15px;
  color: black;
}

.right-container {
  flex: 1;
  max-height: 100%; /* 부모 컨테이너의 높이를 넘지 않도록 설정 */
  overflow-y: auto; /* 세로 방향 스크롤 가능하도록 설정 */
  overflow-x: hidden; /* 가로 방향 스크롤 방지 */
}

.movies-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: space-between;
}

.movie-card {
  flex: 1 0 calc(33.33% - 10px); /* 3열 레이아웃 설정 (gap 고려) */
  box-sizing: border-box;
}

.movie-img {
  width: 100%; /* 부모의 너비를 꽉 채움 */
  position: relative;
  padding-top: calc((5 / 3) * 100%); /* 영화 포스터의 적절한 비율로 높이 설정 */
  overflow: hidden; /* 튀어나가는 부분 잘라내기 */
  position: relative;
}

.movie-img img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

</style>
