import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ Google Maps API Key 설정
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"

# ✅ 허용된 검색 키워드 목록 (파충류 관련)
VALID_ANIMAL_KEYWORDS = {
    "파충류", "도마뱀", "뱀", "거북", "악어", "양서류", "이구아나", "카멜레온",
    "특이동물", "특수동물", "희귀동물", "이색동물"
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

# ✅ HTML 태그 제거 함수 (NameError 해결)
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 병원 검색 함수 (네이버 API)
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

# ✅ 검색어 필터링 함수 (지역 + 동물 키워드 반영)
def filter_search_query(user_query):
    filtered_query = "동물병원"

    # ✅ 지역 검색 포함 여부 확인
    for region in REGIONS:
        if region in user_query:
            filtered_query = f"{region} {filtered_query}"
            break

    # ✅ 동물 관련 키워드 포함 여부 확인
    if any(keyword in user_query for keyword in VALID_ANIMAL_KEYWORDS):
        filtered_query = f"파충류 {filtered_query}"

    return filtered_query

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

# ✅ 병원 검색 결과 표시
def display_hospitals():
    user_query = st.session_state.get("hospital_query", "").strip()

    if not user_query:
        st.info("병원 검색어를 사이드바에 입력하세요.")
        return

    # ✅ 검색어 필터 적용
    search_query = filter_search_query(user_query)

    st.title("🏥 병원 검색 결과")
    st.write(f"🔎 검색어: `{search_query}`")

    hospitals = search_hospitals(search_query)

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
        st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")
