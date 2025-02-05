import streamlit as st
from sidebar import render_sidebar
from hospital_page import display_hospitals

# ✅ 앱 초기화 시 세션 상태 초기화
if "hospital_query" not in st.session_state:
    st.session_state["hospital_query"] = ""  # 병원 검색어 기본값

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 병원 검색 결과 렌더링
if selected_option == "병원 검색":
    query = st.session_state.get("hospital_query", "").strip()  # 검색어 가져오기
    if query:  # 검색어가 있을 경우에만 결과 표시
        display_hospitals(query)
    else:
        st.warning("⚠️ 검색어를 입력하세요.")  # 검색어가 없을 경우 경고 메시지
