<template>
  <div class="c-container">
    <div class="background-img" >
      <img v-if="isSelected" :src="getImageUrl(selectedMovie.backdrop_path)" alt="" width="100%">
      <img v-else :src="'https://image.tmdb.org/t/p/original/vukP0Dlib9i09wrlAOHcCP0hXHd.jpg'" width="100%" alt="">
    </div>
    <div class="left-container">
      <div v-if="isSelected">
        <div class="img-container">
          <img :src="getImageUrl(selectedMovie.poster_path)" alt="" width="100%">
          <div class="search-container">
            <div class="selectedMovie-title">{{ selectedMovie.title }}</div>
            <div type="button" class="search-btn" data-bs-toggle="modal" data-bs-target="#exampleModal">
              <div>Search</div>
            </div>
          </div>
        </div>  
      </div>
      <div v-else>
        <div class="img-container before-img">
          <img :src="'https://image.tmdb.org/t/p/original/vukP0Dlib9i09wrlAOHcCP0hXHd.jpg'" alt="Movie Image" height="100%">
          <div class="search-container">
            <div>Search your movie and start sharing your thoughts.</div>
            <div type="button" class="search-btn" data-bs-toggle="modal" data-bs-target="#exampleModal">
              <div>Search</div>
          </div>
        </div>
        </div>
      </div>
    </div>

    <div class="right-container">
      <div class="right-inner">
        <div class="create-txt">CREATE ARTICLE</div>
        <form @submit.prevent="createArticle" class="create-form">
          <div class="title-input">
            <input type="text" id="title" v-model.trim="title" placeholder="type your article title">
          </div>
          <textarea id="content" v-model.trim="content" placeholder="content"></textarea>
          <div class="btn-container">
            <button type="submit" class="btn btn-warning submit-btn">SUBMIT</button>
          </div>
        </form>
      </div>
    </div>
  </div>
    <!-- modal -->
  <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">영화 검색</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body">
          <form @submit.prevent="searchMovie(movieTitle)" class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Recipient's username" aria-label="Recipient's username" aria-describedby="button-addon2" v-model="movieTitle">
            <button class="btn btn-outline-secondary" type="submit" id="button-addon2">Button</button>
          </form>
          <div class="modal-body-item">
            <SearchedMovieList @update-selected="handleSelectedTitle" v-if="showMovieList"/>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <input type="button" @click="checkImg" class="btn btn-primary" value="Save changes" data-bs-dismiss="modal">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter' 
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'
import { useRouter } from 'vue-router'
import SearchedMovieList from '@/components/SearchedMovieList.vue'


// 영화 검색하는 코드
const movieStore = useMovieStore()
const movieTitle = ref('')
const showMovieList = ref(false);
const searchMovie = () => {
  movieStore.searchMovies(movieTitle.value)
  showMovieList.value = true;
}

const selectedMovie = ref(null)
const handleSelectedTitle = (movie) => {
  selectedMovie.value = movie;
};

//영화 이미지 업로드
const isSelected = ref(false)
const checkImg = () => {
  if(selectedMovie){
    isSelected.value = true
  }
}
const getImageUrl = (posterPath) => {
  return posterPath ? `https://image.tmdb.org/t/p/w500${posterPath}` : '/placeholder.jpg';
};

// Article 만드는 코드
const title = ref(null)
const content = ref(null)

const counterStore = useCounterStore()
const router = useRouter()

// DRF로 게시글 생성 요청을 보내는 함수
const createArticle = function () {
  axios({
    method: 'post',
    url: `${counterStore.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value,
      movie_id: selectedMovie.value.id
    },
    headers: {
      Authorization: `Token ${counterStore.token}`
    }
  })
    .then((res) => {
      // console.log('게시글 작성 성공!')
      router.push({ name: 'ArticleView' })
      console.log("create에서 선택된 영화 ",selectedMovie.value)
    })
    .catch((err) => {
      console.log(err)
    })
}



</script>

<style scoped>
.modal-body-item {
  overflow-x: auto;
}

.c-container {
  display: flex;
  width: 100vw;
  height: 90vh;
  flex-wrap: wrap;
  padding: 5rem;
  gap: 3rem
}

.left-container {
  position: relative;
  display: flex;
  align-items: center;
}

.img-container {
  display: flex;
  justify-content: center;
  width: 30rem;
  height: 42rem;
  overflow: hidden;
  border-radius: 30px;
  filter: grayscale(10%) brightness(60%);
  transition: filter 0.2s ease-in-out;
}


.left-container:hover .img-container {
  filter: grayscale(10%) brightness(70%);
}

.search-container {
  display: flex;
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.search-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 8rem;
  padding: 0.7rem 0;
  border-radius: 20px;
  transition: all 0.3s ease-in-out;
  background-color: rgba(255, 255, 255, 0.1);
}

.search-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.search-btn:hover .before-img {
  filter: grayscale(10%) brightness(50%);
}

.selectedMovie-title {
  font-size: 1.3rem;
  font-weight: 700;
}

.right-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: center;
}

.right-inner {
  display: flex;
  flex-direction: column;
  color: rgb(240, 240, 240);
  background-color: rgba(120, 120, 120, 0.4);
  border-radius: 25px;
  min-width: 0rem;
  height: 42rem;
  padding: 2rem;
}

.create-txt {
  font-size: 3rem;
  font-weight: 100;
}

.create-form {
  flex: 1;
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.title-input {
  border-bottom: 2px solid white;
}

#title {
  width: 100%;
  background: none;
  border-bottom: 2px solid white;
  border: none;
  border-radius: 5px;
  padding: 0.5rem 0.3rem;
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 200;
}

#content {
  padding: 0.5rem 0.3rem;
  color: rgba(255, 255, 255, 0.7);
  border-radius: 5px;
  font-size: 1.2rem;
  font-weight: 200;
  background: none;
  flex: 1;
}

.submit-btn {
  width: 7rem;
}

.btn-container {
  display: flex;
  flex-direction: row-reverse;
}

.background-img {
  width: 100vw;
  height: 100%;
  position: absolute;
  filter: blur(15px) brightness(20%);
  z-index: -1;
}


</style>
