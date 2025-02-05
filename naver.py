import requests
import streamlit as st

NAVER_CLIENT_ID = "OoSMwYAOM2tdBLryoPR7"
NAVER_CLIENT_SECRET = "Rg1UhuYeCM"
NAVER_API_URL = "https://openapi.naver.com/v1/search/local"

# 🏥 파충류 전문 병원 검색 함수
def search_hospitals(query="파충류 동물병원", display=5):
    try:
        headers = {
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        }
        params = {
            "query": query,
            "display": display,
            "sort": "random",
        }
        response = requests.get(NAVER_API_URL, headers=headers, params=params, timeout=5)

        if response.status_code == 200:
            items = response.json().get("items", [])
            reptile_keywords = ["파충류", "도마뱀", "이구아나", "거북", "뱀", "동물병원"]
            return [item for item in items if any(kw in item["title"] for kw in reptile_keywords)]
        else:
            st.error(f"❌ API 호출 실패: 상태 코드 {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 네트워크 오류: {e}")
        return []
