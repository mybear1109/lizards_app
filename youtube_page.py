import streamlit as st
import requests

# 유튜브 API 설정
YOUTUBE_API_KEY = "AIzaSyC4lXnmvmSeZy5pCoxDddwMgVxNnKbB9CA"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube_videos(query="파충류 사육", max_results=5):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }
    try:
        response = requests.get(YOUTUBE_API_URL, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error(f"API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except Exception as e:
        st.error(f"네트워크 오류: {e}")
        return []

def display_youtube_videos(query):
    st.title("📺 유튜브 검색 결과")
    videos = search_youtube_videos(query)
    if videos:
        for video in videos:
            video_id = video["id"]["videoId"]
            title = video["snippet"]["title"]
            description = video["snippet"].get("description", "설명 없음")
            link = f"https://www.youtube.com/watch?v={video_id}"
            st.markdown(f"### [{title}]({link})")
            st.write(description)
    else:
        st.write("검색 결과가 없습니다.")
