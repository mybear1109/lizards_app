import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 네이버 API 설정 (병원 검색 및 연락처 조회)
NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_SEARCH_API_URL = "https://openapi.naver.com/v1/search/local.json"

# ✅ 네이버 검색 URL을 병원이름에 맞춰 자동 생성
def get_naver_search_url(hospital_name):
    """ 네이버 검색 URL 생성 (병원이름 기반) """
    query = urllib.parse.quote(hospital_name)
    return f"https://search.naver.com/search.naver?query={query}"

# ✅ Google Maps API 설정 (지도 표시)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyAb7sspwz8bq-OvQCt-pP9yvRVHA0zkxqw")


# ✅ HTML 태그 제거 함수
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# ✅ 네이버 상세보기에서 병원 전화번호 가져오기 (URL 검증 포함)
def get_hospital_contact_from_naver_detail(naver_url):
    """ 네이버 상세보기 페이지에서 전화번호를 가져오는 함수 (URL 오류 방지 포함) """
    
    if not naver_url or not re.match(r"https?://", naver_url):
        return None  # URL이 없거나 형식이 잘못된 경우

    try:
        response = requests.get(naver_url, timeout=5)
        if response.status_code == 200:
            # ✅ 페이지 내에서 전화번호 찾기 (JSON 데이터에서 검색)
            phone_match = re.search(r'\"phone\":\"(.*?)\"', response.text)
            if phone_match:
                return phone_match.group(1)  # ✅ 전화번호 추출
        return None  # 정보가 없을 경우 None 반환
    except Exception as e:
        st.error(f"❌ 네이버 상세보기에서 전화번호 가져오기 실패: {e}")
        return None


# ✅ 병원 검색 API + 네이버 상세보기에서 전화번호 가져오기
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

            # ✅ 병원 상세보기에서 전화번호 가져오기 (URL 확인 포함)
            for hospital in hospitals:
                hospital_name = remove_html_tags(hospital["title"])  # 병원 이름 가져오기
                hospital["link"] = hospital.get("link", get_naver_search_url(hospital_name))  # 네이버 검색 URL 제공
                hospital["telephone"] = get_hospital_contact_from_naver_detail(hospital["link"])

            return hospitals
        else:
            st.error(f"❌ 네이버 병원 검색 실패: {response.status_code}")
            return []
    
    except Exception as e:
        st.error(f"❌ 네트워크 오류 발생: {e}")
        return []


# ✅ Google 지도 Embed 함수 (지도만 구글 API 사용)
def display_hospital_map(address):
    """ 구글 지도에서 병원 위치를 표시하는 함수 """
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
        st.subheader("⚠️ 파충류 관련 병원만 검색할 수 있습니다.")
        st.info("병원 검색어를 사이드바에 입력하세요.")
        return

    st.title("🏥 병원 검색 결과")
    st.write(f"🔎 검색어: `{user_query}`")

    hospitals = search_hospitals(user_query)

    """ 병원 정보를 스타일링하여 표시하는 함수 """
    if hospitals:
        for hospital in hospitals:
            with st.container():
                hospital_name = remove_html_tags(hospital['title'])

                # ✅ 병원명 스타일 변경
                st.markdown(
                    f"""
                    <h3 style="color:#2A9D8F; font-family: 'Arial Black', sans-serif;">
                        🏥 {hospital_name}
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

                # ✅ 주소 정보
                st.markdown(
                    f"""
                    <p style="font-size:16px; color:#264653;">
                        📍 <b>주소:</b> {hospital['address']}
                    </p>
                    """,
                    unsafe_allow_html=True
                )
                display_hospital_map(hospital['address'])  # ✅ 구글 지도 표시

                # ✅ 연락처 정보 (전화번호가 있을 때만 표시)
                if hospital.get('telephone'):
                    st.markdown(
                        f"""
                        <p style="font-size:16px; color:#E76F51;">
                            📞 <b>전화번호:</b> {hospital['telephone']}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                # ✅ 네이버 링크 버튼 스타일 변경 (병원이름 기반 검색 적용)
                st.markdown(
                    f"""
                    <p style="font-size:16px;">
                        <a href="{hospital['link']}" target="_blank"
                        style="text-decoration:none; background-color:#F4A261;
                        color:white; padding:8px 12px; border-radius:5px;
                        font-weight:bold;">
                        🔗 네이버에서 "{hospital_name}" 검색
                        </a>
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                # ✅ 병원 간 구분선 추가
                st.markdown("<hr style='border:1px solid #DADADA; margin:20px 0;'>", unsafe_allow_html=True)
                
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어를 시도해 보세요.")


# ✅ 실행
if __name__ == "__main__":
    display_hospitals()