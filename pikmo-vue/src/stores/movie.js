import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
export const useMovieStore = defineStore('movie', () => {
  const movies = ref([])
  const movies2 = ref([])
  const genres = ref([])
  const streamServices = ref([])
  const movie_detail=ref(null)
  //const API_KEY='155994f7d0eb70b89a91bfa1c7fa84a9'
  const TMDB_KEY = import.meta.env.VITE_TMDB_ACCESS_TOKEN
  const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

  const getMovies = (what) => {
    const options = {
      method: 'GET',
      url: `https://api.themoviedb.org/3/movie/${what}`,
      params: { language: 'ko-kr', page: '1' },
      headers: {
        accept: 'application/json',
        Authorization: `Bearer ${TMDB_KEY}`,
      }
    };

    axios
      .request(options)
      .then(res => {
        if(what === "top_rated"){
          movies.value = res.data.results
          console.log(movies)
        }
        else{
          movies2.value = res.data.results
          console.log(movies2)
        }
      })
      .catch(err => console.error(err));
  }


  // 영화 스트리밍 서비스 정보 가져오기
  const getStreams = async () => {
    const streamsApi = {
      method: 'GET',
      url: 'https://api.themoviedb.org/3/watch/providers/tv',
      params: { watch_region: 'KR' },
      headers: {
        accept: 'application/json',
        Authorization: `Bearer ${TMDB_KEY}`,
      }
    };

    try {
      const response = await axios.request(streamsApi)
      streamServices.value = response.data.results || []  // 스트리밍 서비스 리스트를 저장
    } catch (error) {
      console.error('Failed to fetch streaming services:', error)
    }
  }

  //영화 장르정보 가져오기
  const getGenres = async () => {
    const genresApi = {
      method: 'GET',
      url: 'https://api.themoviedb.org/3/genre/movie/list',
      params: { language: 'ko-kr' },
      headers: {
        accept: 'application/json',
        Authorization: `Bearer ${TMDB_KEY}`,
      }
    };
    try {
      const response = await axios.request(genresApi);
      genres.value = response.data.genres
    } catch (error) {
      console.error(error)
    }
  }


  const searchedMovies = ref([])
  const searchMovies = (Movietitle) => {
    //const API_KEY='155994f7d0eb70b89a91bfa1c7fa84a9'
    const TMDB_KEY = import.meta.env.VITE_TMDB_ACCESS_TOKEN
    const options = {
      method: 'GET',
      url: 'https://api.themoviedb.org/3/search/movie',
      params: {
        language: 'ko-kr',
        page: '1',
        include_adult: false,
        query: `${Movietitle}`,
      },
      headers: {
        accept: 'application/json',
        Authorization: `Bearer ${TMDB_KEY}`,
      }
    };

    axios
      .request(options)
      .then(res => {
        searchedMovies.value = res.data.results
        console.log(searchedMovies.value.length)
        // console.log(searchedMovies.value)
      })
      .catch(err => console.error(err));

  }

  //영화 가져오기
  const getWatchProviders = async (movieId) => {
    try {
      const response = await axios.get(
        `https://api.themoviedb.org/3/movie/${movieId}/watch/providers`,
        {
          headers: {
            Authorization: `Bearer ${TMDB_KEY}`,
          },
        }
      );

      watchProviders.value[movieId] = response.data.results || {};
      console.log(`Watch Providers for Movie ID ${movieId}:`, watchProviders.value[movieId]);
    } catch (error) {
      console.error(`Failed to fetch watch providers for Movie ID ${movieId}:`, error);
    }
  };




  //유튜브 영상 가져오기
  const getTrailer = async (movieTitle) => {
    const youtubeOptions = {
      method: 'GET',
      url: 'https://www.googleapis.com/youtube/v3/search',
      params: {
        part: 'snippet',
        q: `${movieTitle} official trailer`,
        key: YOUTUBE_API_KEY,
        maxResults: 1,
      },
    };

    try {
      const response = await axios.request(youtubeOptions);
      const videoId = response.data.items[0]?.id?.videoId || null;
      return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
    } catch (error) {
      console.error(`Failed to fetch trailer for ${movieTitle}:`, error);
      return null;
    }
  };

  return { movies, movies2, getMovies, TMDB_KEY, YOUTUBE_API_KEY ,getTrailer, getWatchProviders, genres, getGenres, getStreams, streamServices, searchedMovies, searchMovies}
}, { persist: true })
