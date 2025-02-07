import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "XfPPDZhLop8Yf6wK6trc"
NAVER_CLIENT_SECRET = "XxefLPKZtv"
NAVER_SEARCH_API_URL = "https://openapi.naver.com/v1/search/local"

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
    

# ✅ 병원 검색 결과 표시
def display_hospitals():
    user_query = st.text_input("🔎 병원 검색어를 입력하세요", "")

    if not user_query.strip():
        st.subheader("⚠️ 파충류 관련 병원만 검색할 수 있습니다.")
        st.info("병원 검색어를 입력하세요.")
        return

    st.title("🏥 병원 검색 결과")
    st.write(f"🔎 검색어: `{user_query}`")

    hospitals = search_hospitals(user_query)

    if hospitals:
        for hospital in hospitals:
            hospital_name = remove_html_tags(hospital['title'])  # 병원명
            hospital_address = hospital.get("address", "정보 없음")  # 주소
            hospital_phone = hospital.get("telephone", "").strip()  # 전화번호
            hospital_link = hospital.get("link", "").strip()  # 네이버 블로그 링크

            # ✅ 네이버 링크가 없을 경우 직접 검색 URL 생성
            if not hospital_link:
                hospital_link = get_naver_search_url(hospital_name)

            with st.container():
                # ✅ 병원명 표시
                st.markdown(f"### 🏥 {hospital_name}")

                # ✅ 주소 표시
                st.markdown(f"📍 **주소:** {hospital_address}")

                # ✅ 전화번호가 있을 경우만 표시
                if hospital_phone:
                    st.markdown(f"📞 **전화번호:** {hospital_phone}")

                # ✅ 네이버 병원 검색 링크
                st.markdown(
                    f"[🔗 네이버 병원 검색]({hospital_link})",
                    unsafe_allow_html=True
                )

                # ✅ 병원 간 구분선 추가
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