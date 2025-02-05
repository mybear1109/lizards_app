import requests
import streamlit as st

YOUTUBE_API_KEY = "AIzaSyC4lXnmvmSeZy5pCoxDddwMgVxNnKbB9CA"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

# 📺 파충류 관련 유튜브 영상 검색 함수
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
            videos = response.json().get("items", [])
            return [
                {
                    "title": video["snippet"]["title"],
                    "description": video["snippet"].get("description", "설명 없음"),
                    "link": f"https://www.youtube.com/watch?v={video['id']['videoId']}",
                }
                for video in videos if "videoId" in video["id"]
            ]
        else:
            st.error(f"❌ YouTube API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 네트워크 오류: {e}")
        return []
