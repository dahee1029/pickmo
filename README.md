### 프로젝트 개요

- 설명 : 영화 추천 서비스
- 기간 : 2024.11.18(월) ~ 2023.11.26(화)

### 서비스 특징

- 유저의 감정을 분석하고 공감해주면서 적절한 영화 ost추천
- 감성적인 영화 추천 사이트

### 주요 기능

- 영화 정보
- 커뮤니티 (게시글 작성, 댓글작성)
- 챗봇 (유저의 감정을 분석하고 공감해주면서 적절한 영화 os추천)
- 유저 프로필

### 팀 소개

| 안다정              | 임다희              |
| ------------------- | ------------------- |
| 팀장, 프론트,백엔드 | 팀원, 프론트,백엔드 |

## 기술 스택

### Backend

![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=django&logoColor=white)&nbsp;
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)&nbsp;

### Frontend

![Vue.js](https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)&nbsp;

### Tools

![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)&nbsp;
![VS code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)&nbsp;
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)&nbsp;

<br />

## 🔧 개발 환경

**Backend**

- django 4.2.4

**Frontend**

- vue.js 3.3.4

<br/>

## 프로젝트 폴더 구조

- Backend - Django

```
pickmo_django
├─accounts
├─articles
├─movies
└─pickmo_django_project
```

- Frontend - Vue.js

```
pickmo-vue
├─.vscode
├─node_modules
├─public
└─src
    ├─assets
    ├─components
    ├─router
    ├─stores
    └─views
        ├─ArticleDetailView.vue
        ├─ArticleView,.vue
        ├─ChatBotView.vue
        ├─CreateView.vue
        ├─HomeView.vue
        ├─LoginView.vue
        ├─MovieDetailView.vue
        ├─MovieListView.vue
        ├─RecommmendedView.vue
        ├─SignUpView.vue
        ├─UpdatePasswordView.vue
        ├─UpdateProfileView.vue
        ├─UserProfileView.vue
        └─etc..
```

<br/>

### 코드 컨벤션

<details>
<summary><b>명명법</b></summary>

- 프론트엔드

  - 변수명, 메서드명
    - `camelCase`
  - HTML 템플릿
    - `kebab-case`
  - CSS 클래스
    - 고유한 클래스명 부여하여 부모 컴포넌트 내의 속성 상속을 방지
  - 의미없는 변수명 사용 지양

- 백엔드 - 클래스명 - `PascalCase` - 함수명 - `snake_case` - 의미없는 변수명 사용 지양
</details>

<br/>

## 기능 상세 설명

### 첫 페이지 & 메인 페이지

- 메인 페이지: 현재 상영 중인 영화 및 인기 영화 표(포스터, 제목, 개요)
- TMDB API 사용, axios를 통한 데이터 호출

### Navbar 기능

- 페이지 이동 버튼
- 검색 버튼: 입력한 영화 제목과 일치하는 포스터 목록 표시
  로그인/로그아웃 상태에 따른 Navbar 버튼 변화

### 추천 페이지

- - 유저 입력(장르, OTT 서비스) 기반 영화 리스트 조회

### PickBot 페이지

- ChatGPT API 활용 챗봇
- 유저 기분에 따른 공감 및 영화 OST 추천

### 커뮤니티 페이지

- 게시글 작성 기능
- 카드형 게시글 리스트, 영화 상세/게시글 상세로 이동 가능

### 영화 상세 페이지

- 영화 정보(제목, 런타임, 장르, OTT 서비스 등) 제공
- 예고편 모달
- 좋아요/취소 버튼으로 유저 프로필에 영화 추가

### 유저 프로필 페이지

- 사용자 정보 및 좋아요한 영화 목록 확인
- 프로필 수정 및 비밀번호 변경 기능

### 프로필 수정 & 비밀번호 변경 페이지

- 사용자 정보 수정
  비밀번호 변경(현재 비밀번호, 새 비밀번호 확인 필수)

## 주요 기술과 API 활용

- TMDB API: 영화 데이터
- ChatGPT API: 챗봇 기능
- Django: 백엔드 구현
- Vue: 프론트엔드 구축

<br />

## API 입력 위치

```
django_project/.env
TMDB_API_KEY= ""
YOUTUBE_API_KEY= ""
```
