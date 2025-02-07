import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ Streamlit 페이지 설정 (최상단에 위치)
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_SEARCH_API_URL = "https://openapi.naver.com/v1/search/local"

# ✅ 네이버 검색 URL을 병원이름에 맞춰 자동 생성
def get_naver_search_url(hospital_name):
    query = urllib.parse.quote(hospital_name)
    return f"https://search.naver.com/search.naver?query={query}"

# ✅ HTML 태그 제거
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 병원 검색 API
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
    address_encoded = urllib.parse.quote(address)
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY")
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY":
        map_embed_url = f"https://www.google.com/maps/embed/v1/place?key={AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw}&q={address_encoded}"
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
        st.error("⚠️ Google Maps API Key가 설정되지 않았습니다.")

# ✅ 병원 검색 결과 표시
def display_hospitals(query):
    hospitals = search_hospitals(query)
    if hospitals:
        for hospital in hospitals:
            hospital_name = remove_html_tags(hospital['title'])
            hospital_address = hospital.get("address", "정보 없음")
            hospital_link = hospital.get("link", get_naver_search_url(hospital_name))

            with st.container():
                # 병원명
                st.markdown(f"### 🏥 {hospital_name}")
                # 주소
                st.markdown(f"📍 **주소:** {hospital_address}")
                # 구글 지도 표시
                display_hospital_map(hospital_address)
                # 네이버 병원 검색 링크
                st.markdown(
                    f"[🔗 네이버 병원 검색]({hospital_link})",
                    unsafe_allow_html=True,
                )
                # 구분선
                st.markdown("---")
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")

# ✅ 실행
if __name__ == "__main__":
    # 사이드바에 검색 입력 추가
    st.sidebar.header("병원 검색")
    user_query = st.sidebar.text_input("🔎 검색어 입력", "파충류 동물병원")
    st.sidebar.write("검색어를 입력한 후 결과는 바로 표시됩니다.")
    
    # 결과 표시
    display_hospitals(user_query)