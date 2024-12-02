<template>
    <div>
        <div v-if="store.searchedMovies.length > 0" class="movie-list">
            <div v-for="movie in store.searchedMovies" :key="movie.id" class="movie-item">
                <img
                    v-if="movie.poster_path"
                    :src="`https://image.tmdb.org/t/p/w200/${movie.poster_path}`"
                    :alt="movie.title"
                    class="movie-poster"
                    @click="selectImg(movie)"
                />
            <!-- <p>{{ movie.title }}</p> -->
            </div>
        </div>
        <p v-else>검색 결과가 없습니다.</p>
        <div v-if="isSelected">
            {{selectedTitle}}
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useMovieStore } from '@/stores/movie';

const emit = defineEmits(['update-selected']);

const store = useMovieStore()
const isSelected = ref(false)
const selectedTitle = ref('')

const selectImg = (movie) => {
    console.log(movie)
    isSelected.value = true
    selectedTitle.value = movie.title

    emit('update-selected', movie);
}


</script>

<style scoped>
.movie-list {
    padding: 10px 0;
    display: flex;
    flex-direction: row;
    gap: 12px;
    overflow-x: auto;
}

.movie-item {
  display: inline-block;
}

.movie-poster {
  display: block;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 5px;
}

.movie-poster:hover {
  transform: translateY(-10px); /* 이미지가 위로 올라가는 효과 */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}
</style>