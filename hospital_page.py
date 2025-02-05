import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ Google Maps API Key 설정
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"

# ✅ 네이버 API를 이용한 병원 검색
def search_hospitals(query="파충류 동물병원", display=5):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}
    try:
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error(f"❌ API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []

# ✅ Google 지도 Embed 함수
def display_hospital_map(address):
    address_encoded = urllib.parse.quote(address)
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY":
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
        st.error("⚠️ Google Maps API Key가 설정되지 않았습니다.")

# ✅ HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 병원 검색 결과 표시
def display_hospitals():
    query = st.session_state.get("hospital_query", "").strip()

    if not query:
        st.warning("검색어를 입력하세요.")
        return

    st.title("🏥 병원 검색 결과")
    hospitals = search_hospitals(query)

    if hospitals:
        for hospital in hospitals:
            with st.container():
                hospital_name = remove_html_tags(hospital['title'])
                st.markdown(f"### 🏥 {hospital_name}")
                st.write(f"📍 **주소**: {hospital['address']}")
                display_hospital_map(hospital['address'])
                st.write(f"📞 **전화번호**: {hospital.get('telephone', '정보 없음')}")
                st.markdown(f"[🔗 네이버 상세보기]({hospital['link']})", unsafe_allow_html=True)
                st.divider()
    else:
        st.warning("검색 결과가 없습니다. 다시 검색해 주세요.")