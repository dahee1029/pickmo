<template>
    <div class="a-container">
      <div class="community-txt"><div>CO<span class="mm-txt">MM</span>UNITY</div></div>
      <div class="create-btn-wrapper"><RouterLink :to="{ name: 'CreateView' }" class="create-btn">CREATE</RouterLink></div>
      <div class="card-container">
        <ArticleListItem 
          v-for="article in store.articles"
          :key="article.id"
          :article="article"
        />
      </div>
    </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
})
</script>

<style scoped>
* {font-family: "Noto Sans KR", sans-serif;;}

a {
  text-decoration: none; /* 밑줄 제거 */
  color: inherit; /* 부모 요소의 색상 상속 */
}

.a-container {
  display: flex;
  flex-direction: column;
}

.card-container {
  display: flex;
  padding: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
  }

.community-txt {
  padding: 2rem 0 0 0;
  font-size: 3.5rem;
  display: flex;
  justify-content: center;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 300;
  opacity: 0.8;
}

.mm-txt {
  color: #ffb703;
}


.create-btn-wrapper {
  display: flex;
}

.create-btn {
  transition: all ease-in-out 0.3s;
  box-sizing: content-box;
  border: 2px solid white;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
  font-weight: 500;
  padding: 0.7rem 1rem;
  border-radius: 15px;
  margin-left: 1.5rem;
  opacity: 0.8;
}

.create-btn:hover {
  color: rgba(0, 0, 0, 0.9);
  background-color: white;

}

</style>
  