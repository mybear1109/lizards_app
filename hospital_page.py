import re
import os
import requests
import streamlit as st
import urllib.parse
from datetime import datetime

# ✅ Google Maps API Key 설정
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"
NAVER_BLOG_API_URL = "https://openapi.naver.com/v1/search/blog.json"

# ✅ 병원 검색 가능한 지역 및 키워드
VALID_ANIMAL_KEYWORDS = {"파충류", "도마뱀", "뱀", "거북", "악어", "양서류", "이구아나", "카멜레온", "특이동물", "특수동물", "희귀동물", "이색동물"}

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

# ✅ HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 네이버 병원 검색 함수
def search_hospitals(query="파충류 동물병원", display=5):
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": query, "display": display}
    try:
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            st.error(f"❌ 네이버 병원 검색 실패: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []

# ✅ 네이버 블로그 검색 함수
def search_naver_blog(query):
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": query, "display": 5, "sort": "date"}
    response = requests.get(NAVER_BLOG_API_URL, headers=headers, params=params)
    return response.json()

# ✅ Google 지도 Embed 함수
def display_hospital_map(address):
    address_encoded = urllib.parse.quote(address)
    if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY":
        map_embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={address_encoded}"
        st.markdown(
            f"""
            <iframe src="{map_embed_url}" width="100%" height="250" style="border-radius:10px; border:0;" allowfullscreen="" loading="lazy"></iframe>
            """,
            unsafe_allow_html=True,
        )

# ✅ 병원 검색 UI 및 결과 출력
def display_hospitals():
    st.title("🏥 파충류 병원 검색")
    
    location = st.text_input("지역을 입력하세요 (예: 서울, 경기)")
    animal_type = st.selectbox("파충류 종류를 선택하세요", ["도마뱀", "뱀", "거북", "양서류", "기타"])
    service_type = st.multiselect("필요한 서비스", ["24시간", "야간진료", "응급진료"])
    
    if st.button("🔍 병원 검색"):
        search_query = f"{location} {animal_type} 파충류 동물병원 특수동물 병원 {' '.join(service_type)}"
        hospitals = search_hospitals(search_query)

        if hospitals:
            for hospital in hospitals:
                with st.container():
                    hospital_name = remove_html_tags(hospital['title'])

                    st.markdown(
                        f"""
                        <h3 style="color:#2A9D8F; font-family: 'Arial Black', sans-serif;">
                            🏥 {hospital_name}
                        </h3>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <p style="font-size:16px; color:#264653;">
                            📍 <b>주소:</b> {hospital['address']}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )
                    display_hospital_map(hospital['address'])

                    st.markdown(
                        f"""
                        <p style="font-size:16px; color:#E76F51;">
                            📞 <b>전화번호:</b> {hospital.get('telephone', '정보 없음')}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <p style="font-size:16px;">
                            <a href="{hospital['link']}" target="_blank"
                            style="text-decoration:none; background-color:#F4A261;
                            color:white; padding:8px 12px; border-radius:5px;
                            font-weight:bold;">
                            🔗 네이버 상세보기
                            </a>
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown("<hr style='border:1px solid #DADADA; margin:20px 0;'>", unsafe_allow_html=True)
        else:
            st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")

# ✅ 네이버 블로그 검색 UI 및 결과 출력
def display_naver_blog_search():
    st.subheader("📝 네이버 블로그 검색")
    user_query = st.text_input("검색어 입력 (예: 파충류 병원, 이구아나 진료 후기)")

    if st.button("🔍 블로그 검색"):
        blog_results = search_naver_blog(user_query)

        if "items" in blog_results:
            for item in blog_results["items"]:
                st.markdown(
                    f"""
                    <h4 style="color:#2A9D8F;">📌 {remove_html_tags(item['title'])}</h4>
                    <p>📝 {remove_html_tags(item['description'])}</p>
                    <p>📅 {datetime.strptime(item['postdate'], "%Y%m%d").strftime("%Y-%m-%d")}</p>
                    <a href="{item['link']}" target="_blank"
                    style="text-decoration:none; background-color:#E76F51; color:white;
                    padding:8px 12px; border-radius:5px; font-weight:bold;">
                    🔗 블로그 보기
                    </a>
                    <hr style='border:1px solid #DADADA; margin:20px 0;'>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("검색 결과가 없습니다.")

# ✅ 스트림릿 실행
def main():
    st.sidebar.title("🔍 검색 옵션")
    page = st.sidebar.radio("검색 유형 선택", ["🏥 병원 검색", "📝 블로그 검색"])

    if page == "🏥 병원 검색":
        display_hospitals()
    elif page == "📝 블로그 검색":
        display_naver_blog_search()

if __name__ == "__main__":
    main()