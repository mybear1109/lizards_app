import streamlit as st
import requests
import re

# ✅ 유튜브 API 설정
YOUTUBE_API_KEY = "AIzaSyC4lXnmvmSeZy5pCoxDddwMgVxNnKbB9CA"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

# ✅ 허용된 검색 키워드 목록 (한글/영어 포함)
SEARCH_TERMS = [
    "Beardy Dragon", "Panther Chamaeleon", "Crestedgeko", "Leopardgeko",
    "Iguana", "Other", "Frog", "Salamander", "Snake", "Turtle", "Newt",
    "Pacman", "Toad", "Leachianus Gecko", "Gecko", "Chahoua Gecko",
    "Gargoyle Gecko", "Skink", "Chamaeleon", "비어디 드래곤", "팬서 카멜레온",
    "크레스티드 게코", "레오파드 게코", "이구아나", "기타", "개구리", "도롱뇽",
    "뱀", "거북이", "뉴트", "팩맨 개구리", "두꺼비", "리치아누스 게코",
    "도마뱀붙이", "차후아 게코", "가고일 게코", "스킨크", "카멜레온",
    "파충류", "서식지", "생태", "도마뱀", "악어", "파충류 관련", "파충류 정보", "파충류 관련 영상",
    "게코", "개코", "도마뱀 모프", "성체"
]

# ✅ 검색어 필터링 함수
def search_text(text, terms=SEARCH_TERMS):
    """ 사용자가 입력한 검색어가 허용된 키워드 목록에 포함되는지 확인 """
    found_terms = []
    for term in terms:
        if re.search(term, text, re.IGNORECASE):  # 대소문자 구분 없이 검색
            found_terms.append(term)
    return found_terms

# ✅ 유튜브 검색 API 호출 함수
def search_youtube_videos(query, max_results=5):
    """ 유튜브 API를 통해 검색어에 해당하는 동영상을 가져옴 """
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
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []

# ✅ 유튜브 검색 결과 표시 함수
def display_youtube_videos():
    """ 유튜브 검색 결과를 Streamlit 앱에 표시하는 함수 """
    query = st.sidebar.text_input("📺 유튜브 검색어 입력", "파충류 사육 방법", key="youtube_query").strip()

    if not query:
        st.subheader("⚠️ 파충류 관련 영상만 검색할 수 있습니다.")
        st.info("유튜브 검색어를 입력하고 결과를 확인하세요.")
        return

    # ✅ 허용된 키워드 검색 제한
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

            # ✅ 동영상 제목과 링크 추가
            st.markdown(f"### [{title}]({link})")
            st.write(description)

            # ✅ 유튜브 동영상 임베드 (자동 실행 방지)
            video_embed = f"""
                <iframe width="100%" height="315" 
                    src="https://www.youtube.com/embed/{video_id}" 
                    frameborder="0" allow="accelerometer; autoplay; 
                    encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
                </iframe>
            """
            st.markdown(video_embed, unsafe_allow_html=True)

            # ✅ 구분선 추가
            st.divider()
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
