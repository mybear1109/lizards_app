import streamlit as st
import requests

# ✅ 유튜브 API 설정
YOUTUBE_API_KEY = "AIzaSyC4lXnmvmSeZy5pCoxDddwMgVxNnKbB9CA"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
# ✅ 유튜브 검색 함수
def search_youtube_videos(query, max_results=5):
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
            st.error(f"❌ API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []

# ✅ 유튜브 검색 결과 표시 함수
def display_youtube_videos():
    query = st.session_state.get("youtube_query", "파충류 사육").strip()
    if not query:
        st.info("유튜브 검색어를 사이드바에서 입력하세요.")
        return
    
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
            
            # 유튜브 영상 임베드
            st.video(link)
            st.divider()
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")