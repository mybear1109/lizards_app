import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ Google Maps API Key (환경 변수 사용, 보안을 위해 직접 하드코딩하지 않음)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")  # 여기에 본인의 API Key를 입력하세요.

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
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
    """Google Maps Embed API를 통해 병원 위치를 표시"""
    address_encoded = urllib.parse.quote(address)
    
    # ✅ 지도 iframe 생성
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "YAIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw":
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
        st.error("⚠️ Google Maps API Key가 설정되지 않았습니다. `.env` 파일 또는 환경 변수에서 설정하세요.")
    
    # ✅ 추가: Google Maps에서 직접 보기 링크 제공
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={address_encoded}"
    st.markdown(f"[📍 Google 지도에서 보기]({google_maps_url})", unsafe_allow_html=True)

def remove_html_tags(text):
    """문자열에서 HTML 태그 제거"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 병원 검색 결과 표시 함수
def display_hospitals(query):
    st.title("🏥 병원 검색 결과")
    hospitals = search_hospitals(query)

    if hospitals:
        for hospital in hospitals:
            with st.container():
                hospital_name = remove_html_tags(hospital['title'])
                st.markdown(f"### 🏥 {hospital_name}")
                st.write(f"📍 **주소**: {hospital['address']}")
                
                # 🗺️ 지도 표시
                display_hospital_map(hospital['address'])

                # 📞 병원 정보
                st.write(f"📞 **전화번호**: {hospital.get('telephone', '정보 없음')}")
                st.markdown(f"[🔗 네이버 상세보기]({hospital['link']})", unsafe_allow_html=True)
                
                st.divider()  # 구분선 추가
    else:
        st.warning("검색 결과가 없습니다. 다시 검색해 주세요.")

# ✅ Streamlit 실행
if __name__ == "__main__":
    st.sidebar.title("🏥 병원 검색")

    # ✅ 사이드바 검색창 추가
    hospital_query = st.sidebar.text_input("🔎 병원 검색어 입력", "파충류 동물병원")
    
    if st.sidebar.button("🔍 검색 실행"):
        st.session_state["query"] = hospital_query  # 검색어를 세션에 저장
        st.success(f"'{hospital_query}' 검색을 실행합니다.")
        display_hospitals(hospital_query)  # 검색 실행
