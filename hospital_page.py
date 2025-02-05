import streamlit as st
import requests
import urllib.parse
import os  # API Key 환경 변수 저장용

# ✅ Google Maps API Key (보안을 위해 환경 변수 사용 추천)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "key=AIzaSyAS_ZTJBz_vkppLJu2GkMe6uXy9sCda5")  # 환경 변수에서 불러오기

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

# ✅ 지도 Embed 함수
def display_hospital_map(address):
    """구글 지도 API를 통해 병원 위치를 화면에 삽입"""
    address_encoded = urllib.parse.quote(address)
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

# ✅ 병원 검색 결과 표시 함수
def display_hospitals(query):
    st.title("🏥 병원 검색 결과")
    hospitals = search_hospitals(query)

    if hospitals:
        for hospital in hospitals:
            with st.container():
                st.markdown(f"### 🏥 {hospital['title']}")
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
    hospital_query = st.sidebar.text_input("🔎 검색어 입력", "파충류 동물병원")
    
    if st.sidebar.button("검색"):
        display_hospitals(hospital_query)
