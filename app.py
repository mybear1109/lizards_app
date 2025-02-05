import streamlit as st
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos
from image_analysis import display_image_analysis

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 전환
if selected_option == "홈":
    st.title("🦎 파충류를 종아해서 파충류와 함께하기를 원하는 귀염둥이")
    st.write("""
        - 도마뱀 이미지 분석
        - 파충류 전문 병원 검색
        - 파충류 관련 유튜브 영상 검색
    """)

elif selected_option == "도마뱀 분석":
    display_image_analysis()

elif selected_option == "병원 검색":
    display_hospitals()

elif selected_option == "유튜브 검색":
    display_youtube_videos()
