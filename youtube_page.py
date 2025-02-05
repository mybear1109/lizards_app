import streamlit as st
import requests
import re

# ✅ 유튜브 API 설정
YOUTUBE_API_KEY = "AIzaSyC4lXnmvmSeZy5pCoxDddwMgVxNnKbB9CA" 
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

# ✅ 허용된 검색 키워드 목록 (한글/영어 포함)
search_terms = [
    "Beardy Dragon", "Panther Chamaeleon", "Crestedgeko", "Leopardgeko",
    "Iguana", "Other", "Frog", "Salamander", "Snake", "Turtle", "Newt",
    "Pacman", "Toad", "Leachianus Gecko", "Gecko", "Chahoua Gecko",
    "Gargoyle Gecko", "Skink", "Chamaeleon", "비어디 드래곤", "표범 카멜레온", 
    "크레스티드 게코", "레오파드 게코", "이구아나", "기타", "개구리", "도롱뇽", 
    "뱀", "거북이", "뉴트", "팩맨 개구리", "두꺼비", "리치아누스 게코", 
    "도마뱀붙이", "차후아 게코", "가고일 게코", "스킨크", "카멜레온",
    "파충류", "서식지", "생태", "도마뱀", "악어", "파충류 관련", "파충류 정보",'파충류 관련 영상',
    '게코', '개코','모프','성체'
]

# ✅ 검색어 필터링 함수
def search_text(text, terms=search_terms):
    """ 사용자가 입력한 검색어가 허용된 키워드 목록에 포함되는지 확인 """
    found_terms = []
    for term in terms:
        if re.search(term, text, re.IGNORECASE):  # 대소문자 구분 없이 검색
            found_terms.append(term)
    return found_terms

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
    query = st.session_state.get("youtube_query", "").strip()

    # ✅ 검색어가 비어있을 경우 안내 메시지
    if not query:
        st.info("유튜브 검색어를 사이드바에서 입력하세요.")
        return

    # ✅ 검색어 제한 (허용된 키워드만 검색 가능)
    matched_terms = search_text(query)
    if not matched_terms:
        st.warning("⚠️ 허용된 검색어만 입력 가능합니다! (예: 파충류, 뱀, 서식지, 생태 등)")
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

            # ✅ 유튜브 영상 임베드
            st.video(link)
            st.divider()
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
