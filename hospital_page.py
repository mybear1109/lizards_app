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
    "특이동물", "특수동물", "희귀동물", "이색동물", "파충류 동물병원"
}

# ✅ 지역 목록
REGIONS = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기도", "강원도", "충청북도", "충청남도", "전라북도", "전라남도", "경상북도", "경상남도", "제주도"]

# ✅ 네이버 검색 URL 자동 생성
def get_naver_search_url(hospital_name):
    query = urllib.parse.quote(hospital_name)
    return f"https://search.naver.com/search.naver?query={query}"

# ✅ HTML 태그 제거
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 검색어 필터링
def filter_search_query(user_query):
    """입력된 검색어가 허용된 키워드 또는 지역 목록에 포함되는지 확인"""
    if any(keyword in user_query for keyword in VALID_ANIMAL_KEYWORDS) or any(region in user_query for region in REGIONS):
        return user_query
    else:
        st.warning("⚠️ 허용된 검색어만 입력 가능합니다! (예: 파충류, 도마뱀, 뱀, 거북, 이구아나, 서울, 부산 등)")
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
            return response.json().get("items", [])
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

# ✅ 병원 검색 결과 표시 (검색어 즉시 반영)
def display_hospitals():
    query = st.session_state.get("hospital_query", "파충류 동물병원")  # ✅ session_state에서 검색어 가져오기

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
                st.markdown(f"### 🏥 {hospital_name}")
                st.markdown(f"📍 **주소:** {hospital_address}")
                if hospital_phone:
                    st.markdown(f"📞 **전화번호:** {hospital_phone}")

                # ✅ Google 지도 표시
                display_hospital_map(hospital_address)

                st.markdown(f"[🔗 네이버 상세검색]({hospital_link})", unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")

# ✅ 실행
if __name__ == "__main__":
    st.sidebar.header("🏥 병원 검색")
    display_hospitals()
