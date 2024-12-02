<template>
  <div class="p-container">
    <div class="background-img">
      <img src="https://image.tmdb.org/t/p/original/v9acaWVVFdZT5yAU7J2QjwfhXyD.jpg" alt="" width="100%">
    </div>
    <div class="p-txt">PICKBOT</div>
    <div>Pickbot은 당신의 하루를 특별하게 만들어 줄 감성 영화 OST 추천 챗봇입니다.</div>
    <div class="mb-4">기쁜 일도, 우울한 순간도, 특별한 날도—Pickbot은 당신의 이야기를 듣고 그에 어울리는 영화 음악을 찾아드립니다.</div>
    <div class="chat-container">
      <!-- 검색창 -->
      <div class="search-container">
        <input
          type="text"
          v-model="inputMessage"
          placeholder="오늘 하루에 대해 입력해주세요."
          @keydown.enter="getChatbot"
          class="search-input"
        />
        <button @click="getChatbot" class="search-btn">send</button>
      </div>

      <!-- 로딩 중 표시 (스피너) -->
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
      </div>

      <!-- 검색 결과 -->
      <div class="results-container">
        <div v-for="(message, index) in messages" :key="index" class="result">
          <span v-if="message.role === 'user'" class="user-message">
            {{ message.content }}
          </span>
          <span v-if="message.role === 'assistant'" class="assistant-message">
            {{ message.content }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const messages = ref([
  { role: "assistant", content: "당신의 오늘 하루는 어떠셨나요?" },
]);

const inputMessage = ref("");
const loading = ref(false);
const AI_API_KEY = import.meta.env.VITE_OPENAI_API_KEY;

// 확장된 감정 키워드 설정
const emotionKeywords = {
  positive: [
    "좋아", "행복", "신난다", "기분 좋다", "즐겁다", 
    "뿌듯해", "설렌다", "만족스러워", "활기차", "기대돼"
  ],
  negative: [
    "우울", "슬퍼", "화나", "기분 안 좋아", "속상해", 
    "짜증나", "힘들다", "실망스러워", "지쳤다", "불안해"
  ],
  test: [
    "시험", "떨어졌다", "불합격", "안 풀렸다", 
    "망쳤다", "어려웠다", "긴장돼", "걱정돼", "성적"
  ],
  breakup: [
    "헤어졌다", "이별", "끝났다", "싸웠다", 
    "마음 아프다", "혼자야", "그리워", "추억", "후회돼"
  ],
  neutral: [
    "그냥 그래", "보통이야", "무난해", "별일 없어", 
    "일상적", "평범해", "생각 없어", "잔잔해"
  ],
  celebration: [
    "축하해", "기념일", "승진", "합격", "성공", 
    "좋은 소식", "파티", "환희", "잔치"
  ],
};

const classifyEmotion = (userInput) => {
  userInput = userInput.toLowerCase();

  // 감정 분석
  for (const [emotion, keywords] of Object.entries(emotionKeywords)) {
    if (keywords.some((keyword) => userInput.includes(keyword))) {
      return emotion;
    }
  }
  return "neutral"; // 기본 감정
};

const getChatbot = async () => {
  if (inputMessage.value.trim() === "") return;

  const userMessage = { role: "user", content: inputMessage.value };
  messages.value.push(userMessage);

  const userMood = classifyEmotion(inputMessage.value);
  inputMessage.value = ""; // 입력창 초기화
  loading.value = true;

  try {
    let prompt = "";

    // 감정에 따른 메시지
    switch (userMood) {
      case "positive":
        prompt = "기분이 좋은 상태에 어울리는 영화 OST를 추천해주세요.";
        break;
      case "negative":
        prompt = "우울하거나 슬픈 기분에 어울리는 영화 OST를 추천해주세요.";
        break;
      case "test":
        prompt =
          "시험에서 어려움을 겪은 사람에게 어울리는 영화 OST를 추천해주세요.";
        break;
      case "breakup":
        prompt = "이별한 사람에게 위로가 되는 영화 OST를 추천해주세요.";
        break;
      case "celebration":
        prompt = "축하할 일이 있을 때 듣기 좋은 영화 OST를 추천해주세요.";
        break;
      default:
        prompt = "일반적인 기분에 어울리는 영화 OST를 추천해주세요.";
        break;
    }

    // GPT API 호출
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content:
              "사용자의 기분에 따라 적합한 영화 OST를 추천해주는 챗봇입니다.",
          },
          { role: "assistant", content: prompt },
        ],
      },
      {
        headers: {
          Authorization: `Bearer ${AI_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    const botMessage = response.data.choices[0].message.content;
    messages.value.push({ role: "assistant", content: botMessage });
  } catch (error) {
    console.error(error);
    messages.value.push({
      role: "assistant",
      content: "오류가 발생했습니다. 다시 시도해주세요.",
    });
  } finally {
    loading.value = false;
  }
};
</script>


<style scoped>
* {
  font-family: "Noto Sans KR", sans-serif;
}
/* 전체 컨테이너 스타일 */
/* 전체 컨테이너 스타일 */
.chat-container {
  /* margin-top: 0.7rem; */
  max-width: 50rem;
  width: 40rem;
  min-width: 35rem;
  margin: 0 auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  font-family: 'Arial', sans-serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 70vh;
  border: 1px solid #e6e6e6;
}

/* 검색창 스타일 */
.search-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-top: 1px solid #e6e6e6;
  background-color: #f9f9f9;
}

.search-input {
  width: calc(100% - 80px);
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 25px;
  font-size: 14px;
  background-color: #fff;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  outline: none;
}

.search-input:focus {
  border-color: #3498db;
}

.search-btn {
  background-color: #3498db;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.search-btn:hover {
  background-color: #2874a6;
}

/* 로딩 중 표시 (스피너) */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 대화 내용 스타일 */
.results-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #f8f9fa;
}

.result {
  display: flex;
  margin-bottom: 10px;
  align-items: flex-start;
}

/* 사용자의 메시지 스타일 (오른쪽) */
.user-message {
  background-color: #3498db;
  color: white;
  padding: 12px 18px;
  border-radius: 15px;
  max-width: 70%;
  line-height: 1.5;
  margin-left: auto;
  text-align: right;
  font-size: 14px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.user-message::after {
  content: "";
  position: absolute;
  top: 50%;
  right: -10px;
  width: 0;
  height: 0;
  border-width: 8px;
  border-style: solid;
  border-color: transparent transparent transparent #3498db;
  transform: translateY(-50%);
}

/* 챗봇의 메시지 스타일 (왼쪽) */
.assistant-message {
  background-color: #ffffff;
  color: #333;
  padding: 12px 18px;
  border-radius: 15px;
  max-width: 70%;
  line-height: 1.5;
  margin-right: auto;
  text-align: left;
  font-size: 14px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.assistant-message::after {
  content: "";
  position: absolute;
  top: 50%;
  left: -10px;
  width: 0;
  height: 0;
  border-width: 8px;
  border-style: solid;
  border-color: transparent #ffffff transparent transparent;
  transform: translateY(-50%);
}

/* 스크롤바 스타일 */
.results-container::-webkit-scrollbar {
  width: 8px;
}

.results-container::-webkit-scrollbar-thumb {
  background-color: #bbb;
  border-radius: 4px;
}

.results-container::-webkit-scrollbar-thumb:hover {
  background-color: #999;
}

.p-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 3rem 0;
}

.p-txt {
  font-size: 4rem;
  font-weight: 300;
  margin-bottom: 0.5rem;
}

.background-img {
  position: absolute;
  z-index: -1;
  filter: blur(5px);
  background-color: rgba(0, 0, 0, 0.3);
}

</style>
