import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 네이버 API 설정
NAVER_CLIENT_ID = "YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"

# ✅ 병원 검색
def search_hospitals(query, display=5):
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

# ✅ HTML 태그 제거
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# ✅ 병원 검색 결과 표시
def display_hospitals(query):
    st.title("🏥 병원 검색 결과")
    hospitals = search_hospitals(query)

    if hospitals:
        for hospital in hospitals:
            with st.container():
                hospital_name = remove_html_tags(hospital['title'])
                st.markdown(f"### 🏥 {hospital_name}")
                st.write(f"📍 **주소**: {hospital['address']}")
                st.markdown(f"[🔗 네이버 상세보기]({hospital['link']})", unsafe_allow_html=True)
                st.divider()
    else:
        st.warning("검색 결과가 없습니다. 다시 검색어를 입력하세요.")
