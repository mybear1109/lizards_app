import streamlit as st
from sidebar import render_sidebar
from hospital_page import display_hospitals

# ✅ 앱 실행 시 세션 초기화
if "hospital_query" not in st.session_state:
    st.session_state["hospital_query"] = ""  # 초기 검색어 설정

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 병원 검색 처리
if selected_option == "병원 검색":
    display_hospitals()  # 검색어는 세션 상태에서 가져옴
