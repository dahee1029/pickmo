import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import MovieListView from "@/views/MovieListView.vue";
import MovieDetailView from "@/views/MovieDetailView.vue";
import RecommendedView from "@/views/RecommendedView.vue";
import ArticleView from "@/views/ArticleView.vue";
import ArticleDetailView from "@/views/ArticleDetailView.vue";
import CreateView from "@/views/CreateView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import { useCounterStore } from "@/stores/counter";
import ProfileView from "@/views/UserProfileView.vue";
import UserProfileView from "@/views/UserProfileView.vue";
import UpdateProfileView from "@/views/UpdateProfileView.vue";
import UpdatePasswordView from "@/views/UpdatePasswordView.vue";
import ChatBotView from "@/views/ChatBotView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/movies",
      name: "movies",
      component: MovieListView,
    },
    {
      path: "/:movieId",
      name: "movie_detail",
      component: MovieDetailView,
    },
    {
      path: "/recommended",
      name: "recommended",
      component: RecommendedView,
    },
    {
      path: "/articles",
      name: "ArticleView",
      component: ArticleView,
    },
    {
      path: "/articles/:id",
      name: "ArticleDetailView",
      component: ArticleDetailView,
    },
    {
      path: "/create",
      name: "CreateView",
      component: CreateView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/:user_pk/profile",
      name: "UserProfileView",
      component: UserProfileView,
    },
    {
      path: "/:user_pk/profile/update",
      name: "UpdateProfileView",
      component: UpdateProfileView,
    },
    {
      path: "/:user_pk/profile/update/password",
      name: "UpdatePasswordView",
      component: UpdatePasswordView,
    },
    {
      path: "/chatbot",
      name: "ChatBotView",
      component: ChatBotView,
    },
  ],
});

router.beforeEach((to, from) => {
  const store = useCounterStore();
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === "ArticleView" && !store.isLogin) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === "SignUpView" || to.name === "LogInView") && store.isLogin) {
    window.alert("이미 로그인 되어있습니다.");
    return { name: "ArticleView" };
  }
});

export default router;
