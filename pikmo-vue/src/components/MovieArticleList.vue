<template>
    <div>
      <!-- 게시글이 없을 경우 처리 -->
      <div v-if="articles.length === 0">There are no articles written on this topic.</div>
      <!-- 게시글이 있을 경우 처리 -->
      <div v-else class="article-list">
        <div v-for="article in articles" :key="article.id">
          <RouterLink
            :to="{ name: 'ArticleDetailView', params: { id: article.id } }"
            class="article-inner"
            >
              <div>{{ username }}</div>
              <div>|</div>
              <div>{{ article.title }}</div>
              <!-- <div>{{ article.content }}</div> -->
          </RouterLink>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { RouterLink } from "vue-router";
  import { ref, computed } from "vue";
  import { useRoute,  onBeforeRouteUpdate } from "vue-router";
  import { useCounterStore } from "@/stores/counter";
  import { onMounted } from "vue";
  
  const route = useRoute();
  const movieId = ref(route.params.movieId);
  const counterStore = useCounterStore();
  const articles = ref([]);
  
  const username = computed(() => counterStore.username);

  const getArticles = async () => {
    articles.value = await counterStore.getmovieArticles(movieId.value);
  };
  
  onMounted(() => {
    getArticles();
  });
  
  onBeforeRouteUpdate(async (to, from) => {
    movieId.value = to.params.movieId;
    await getArticles();
  });
  
  </script>
  
  <style scoped>
  a {
    text-decoration: none;
    color: inherit;
  }

  .article-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .article-inner {
    display: flex;
    transition: all ease-in-out 0.3s;
    background-color: rgba(255, 255, 255, 0.2);
    gap: 1rem;
    padding: 5px 0.7rem;
    border-radius: 25px;
    font-size: 1.2rem;
    font-weight: 300;
    padding-left: 1.2rem;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .article-inner:hover {
    background-color: rgba(255, 255, 255, 0.3);

  }
  </style>