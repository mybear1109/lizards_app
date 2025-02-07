import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_SEARCH_API_URL = "https://openapi.naver.com/v1/search/local.json"

# ✅ Google Maps API 설정
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")

# ✅ 허용된 검색 키워드 목록 (파충류 관련)
VALID_ANIMAL_KEYWORDS = {
    "파충류", "도마뱀", "뱀", "거북", "악어", "양서류", "이구아나", "카멜레온",
    "특이동물", "특수동물", "희귀동물", "이색동물", "파충류 동물병원","비어디 드래곤", "표범 카멜레온", 
    "크레스티드 게코", "레오파드 게코", "이구아나", "기타", "개구리", "도롱뇽", 
    "뱀", "거북이", "뉴트", "팩맨 개구리", "두꺼비", "리치아누스 게코", 
    "도마뱀붙이", "차후아 게코", "가고일 게코", "스킨크", "카멜레온",
    "파충류", "서식지", "생태", "도마뱀", "악어",  '게코', '개코','도마뱀 모프','성체'
}

# ✅ 세분화된 지역 목록 (광역시/도 → 시/구/동까지 포함)
REGIONS = [
    "서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
    "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도",
    "경상북도", "경상남도", "제주도",
    # ✅ 서울 주요 구
    "강남구", "서초구", "송파구", "강동구", "강서구", "양천구", "영등포구", 
    "마포구", "종로구", "용산구", "성동구", "광진구", "성북구", "강북구", 
    "도봉구", "노원구", "중랑구", "동대문구", "서대문구", "중구", "은평구", 
    "구로구", "금천구", "동작구",
    # ✅ 경기 주요 도시
    "성남", "수원", "용인", "고양", "부천", "안양", "안산", "평택", "시흥",
    "파주", "의정부", "김포", "광주", "광명", "군포", "이천", "오산", "하남",
    "양주", "구리", "남양주", "여주", "동두천", "포천", "연천",
]
# ✅ 네이버 검색 URL 자동 생성
def get_naver_search_url(hospital_name):
    query = urllib.parse.quote(hospital_name)
    return f"https://search.naver.com/search.naver?query={query}"

# ✅ HTML 태그 제거
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 검색어 필터링 함수 (허용된 검색어만 실행)
def filter_search_query(user_query):
    """입력된 검색어가 허용된 키워드 목록에 포함되는지 확인"""
    if any(keyword in user_query for keyword in VALID_ANIMAL_KEYWORDS):
        return user_query
    else:
        st.warning("⚠️ 허용된 검색어만 입력 가능합니다! (예: 파충류, 도마뱀, 뱀, 거북, 이구아나 등)")
        return None

# ✅ 네이버 API에서 병원 검색
def search_hospitals(query="파충류 동물병원", display=5):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    try:
        response = requests.get(NAVER_SEARCH_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            hospitals = response.json().get("items", [])
            return hospitals
        else:
            st.error(f"❌ 네이버 병원 검색 실패: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []

# ✅ Google 지도 Embed 함수
def display_hospital_map(address):
    """Google 지도에서 병원 위치를 표시하는 함수"""
    address_encoded = urllib.parse.quote(address)

    if GOOGLE_MAPS_API_KEY:
        map_embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={address_encoded}"
        st.markdown(
            f"""
            <iframe 
                src="{map_embed_url}" 
                width="100%" 
                height="250" 
                style="border-radius:10px; border:0;" 
                allowfullscreen="" 
                loading="lazy">
            </iframe>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ Google Maps API Key가 설정되지 않았습니다. 지도 기능을 사용할 수 없습니다.")

# ✅ 병원 검색 결과 표시
def display_hospitals(query="파충류 동물병원"):
    # ✅ 검색어 필터링
    filtered_query = filter_search_query(query)
    if not filtered_query:
        return  # 검색어가 허용되지 않으면 검색 수행 안 함

    hospitals = search_hospitals(filtered_query)

    if hospitals:
        st.title("🏥 병원 검색 결과")
        st.markdown(f"🔎 **검색어:** `{filtered_query}`")

        for hospital in hospitals:
            hospital_name = remove_html_tags(hospital["title"])
            hospital_address = hospital.get("address", "정보 없음")
            hospital_phone = hospital.get("telephone", "").strip()
            hospital_link = hospital.get("link", "").strip()

            # ✅ 네이버 링크가 없을 경우 직접 검색 URL 생성
            if not hospital_link:
                hospital_link = get_naver_search_url(hospital_name)

            with st.container():
                # ✅ 병원명 스타일링
                st.markdown(
                    f"""
                    <h3 style="color:#2A9D8F; font-family: 'Arial Black', sans-serif; margin-bottom: 10px;">
                        🏥 {hospital_name}
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                # ✅ 주소 스타일링
                st.markdown(
                    f"""
                    <p style="font-size:16px; color:#264653; margin-bottom: 10px;">
                        📍 <b>주소:</b> {hospital_address}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                # ✅ 전화번호 표시 (있을 경우만)
                if hospital_phone:
                    st.markdown(
                        f"""
                        <p style="font-size:16px; color:#E76F51; margin-bottom: 10px;">
                            📞 <b>전화번호:</b> {hospital_phone}
                        </p>
                        """,
                        unsafe_allow_html=True,
                    )

                # ✅ Google 지도 표시
                display_hospital_map(hospital_address)

                # ✅ 네이버 병원 상세검색 버튼
                st.markdown(
                    f"""
                    <p style="margin-top: 10px;">
                        <a href="{hospital_link}" target="_blank" 
                        style="text-decoration:none; background-color:#F4A261; 
                        color:white; padding:10px 15px; border-radius:5px; 
                        font-weight:bold;">
                        🔗 네이버 상세검색
                        </a>
                    </p>
                    """,
                    unsafe_allow_html=True,
                )

                # ✅ 병원 간 구분선 추가
                st.markdown("<hr style='border:1px solid #DADADA; margin:20px 0;'>", unsafe_allow_html=True)
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")

# ✅ 실행
if __name__ == "__main__":
    # ✅ 사이드바에 검색 입력 추가
    st.sidebar.header("🏥 병원 검색")
    user_query = st.sidebar.text_input("🔎 검색어 입력", "파충류 동물병원")


# ✅ 유튜브 검색 결과 표시 함수
def display_youtube_videos():
    query = st.session_state.get("youtube_query", "").strip()

    # ✅ 검색어가 비어있을 경우 안내 메시지
    if not query:
        st.subheader("⚠️ 파충류 관련 영상만 검색할 수 있습니다.")
        st.info("유튜브 검색어를 사이드바에서 입력하세요.")
        return

    # ✅ 검색어 제한 (허용된 키워드만 검색 가능)
    matched_terms = search_text(query)
    if not matched_terms:
        st.warning("⚠️ 허용된 검색어만 입력 가능합니다! (예: 파충류, 뱀, 서식지, 생태 등)")
    else:
        display_hospitals("파충류 동물병원")  # 기본 검색어 사용
        return
