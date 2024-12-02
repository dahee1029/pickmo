import { ref, computed, reactive } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore(
  "counter",
  () => {
    //전체 게시글
    const articles = ref([]);
    // // 유저 정보 상태 저장
    const userCache = ref({}); // 캐시 형태로 저장
    const username = ref(null);
    const user_pk = ref(null);
    //특정 영화의 게시글
    const movieArticles = ref([]);
    const API_URL = "http://127.0.0.1:8000";
    const token = ref(null);
    const isLogin = computed(() => {
      if (token.value === null) {
        return false;
      } else {
        return true;
      }
    });
    const router = useRouter();

    const getUsername = function (userId) {
      if (userCache.value[userId]) {
        // 캐시에 유저 데이터가 있으면 반환
        return userCache.value[userId];
      }
      // 없으면 API 호출
      axios({
        method: "get",
        url: `${API_URL}/users/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          console.log(userId);
          const user = res.data.find((user) => user.id === userId);
          if (user) {
            userCache.value[userId] = user.username; // 캐시에 저장
          }
        })
        .catch((err) => {
          console.log(err);
        });
      return userCache.value[userId] || "Loading..."; // API 응답 전에는 로딩 표시
    };

    // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          // console.log(res.data)
          articles.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    //특정 movie의 게시글들 불러오기
    const getmovieArticles = async function (movieId) {
      const res = await axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      return res.data.filter((article) => article.movie_id == movieId);
      // .then((res) => {
      //   movieArticles.value = res.data.filter(
      //     (article) => article.movie_id == movieId
      //   );
      // })
      // .catch((err) => {
      //   console.log(err);
      // });
    };

    // 회원가입 요청 액션
    const signUp = function (payload) {
      // const username = payload.username
      // const password1 = payload.password1
      // const password2 = payload.password2
      const { username, password1, password2, gender } = payload;

      // 비밀번호 확인 로직
      if (password1 !== password2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
      }

      axios({
        method: "post",
        url: `${API_URL}/users/signup/`,
        data: {
          username,
          password1,
          password2,
          gender,
        },
      })
        .then((res) => {
          console.log(res.data);
          // console.log('회원가입 성공')
          const password = password1;
          logIn({ username, password });
        })
        .catch((err) => {
          if (err.response && err.response.data) {
            console.log(err.response.data); // 서버에서 반환된 에러 메시지 확인
            alert("회원가입 실패: " + JSON.stringify(err.response.data)); // 사용자에게 에러 메시지 표시
          } else {
            console.log(err);
            alert("회원가입 중 문제가 발생했습니다.");
          }
        });
    };

    // 로그인 요청 액션
    const logIn = function (payload) {
      // const username = payload.username
      // const password1 = payload.password
      const { username, password } = payload;

      axios({
        method: "post",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          console.log(res);

          token.value = res.data.key;
          fetchUserInfo(); // 사용자 정보 요청 함수 호출
          router.push({ name: "ArticleView" });
          // console.log(res.data)
          // console.log('로그인 성공')
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const fetchUserInfo = function () {
      axios({
        method: "get",
        url: `${API_URL}/accounts/user/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          console.log("사용자 정보 요청 성공", response);
          user_pk.value = response.data.pk;
          username.value = response.data.username;
        })
        .catch((error) => {
          console.log("사용자 정보 가져오기 실패", error);
        });
    };

    // [추가기능] 로그아웃
    const logOut = function () {
      axios({
        method: "post",
        url: `${API_URL}/accounts/logout/`,
      })
        .then((res) => {
          console.log(res.data);
          token.value = null;
          router.push({ name: "ArticleView" });
        })
        .catch((err) => {
          console.log(err);
        });
    };
    return {
      articles,
      API_URL,
      movieArticles,
      getmovieArticles,
      getUsername,
      getArticles,
      signUp,
      logIn,
      token,
      isLogin,
      logOut,
      user_pk,
      username,
    };
  },
  { persist: true }
);
