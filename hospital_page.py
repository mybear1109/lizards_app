import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local.json"  # 오타 수정

# ✅ Google Maps API 설정
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")

# ✅ 네이버 검색 URL 자동 생성
def get_naver_search_url(hospital_name):
    query = urllib.parse.quote(hospital_name)
    return f"https://search.naver.com/search.naver?query={query}"

# ✅ HTML 태그 제거
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 네이버 API에서 병원 검색
def search_hospitals(query="파충류 동물병원", display=5):
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}
    
    try:
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=5)
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
        st.warning("⚠️ Google Maps API Key가 설정되지 않았습니다. 지도 기능을 사용할 수 없습니다.")

# ✅ 병원 검색 결과 표시
def display_hospitals():
    """ 병원 검색 및 결과 표시 함수 """
    user_query = st.sidebar.text_input("🔎 검색어 입력", "파충류 동물병원")

    hospitals = search_hospitals(user_query)

    if hospitals:
        st.title("🏥 병원 검색 결과")
        st.markdown(f"🔎 **검색어:** `{user_query}`")

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
