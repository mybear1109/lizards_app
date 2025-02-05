import streamlit as st
from image_analysis import display_image_analysis  # 올바른 모듈 import
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 렌더링
if selected_option == "홈":
    st.title("🦎 파충류 검색 앱")
    st.write("이 앱은 도마뱀 이미지 분석, 병원 검색, 유튜브 검색 기능을 제공합니다.")
elif selected_option == "도마뱀 분석":
    display_image_analysis()
elif selected_option == "병원 검색":
    query = st.text_input("검색어를 입력하세요", "파충류 동물병원")
    if st.button("검색"):
        display_hospitals(query)
elif selected_option == "유튜브 검색":
    query = st.text_input("검색어를 입력하세요", "파충류 사육")
    if st.button("검색"):
        display_youtube_videos(query)
