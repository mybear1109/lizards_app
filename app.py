import os
import streamlit as st
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos
from image_analysis import display_image_analysis # type: ignore

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 전역 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ 페이지 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ✅ 홈 페이지 렌더링 함수
def display_home():
    col1, col2 = st.columns([1, 2])

    with col1:
        image_path = os.path.join(BASE_DIR, "image", "001.jpg")
        if os.path.exists(image_path):
            st.image(image_path, width=300)
        else:
            st.error("❌ 홈 화면 이미지 파일이 없습니다.")

    with col2:
        st.title("🦎 안녕하세요 파충류 앱입니다.")
        st.write("""

        """)

# ✅ 사이드바 렌더링 및 선택 메뉴 처리
selected_option = render_sidebar()

# 선택된 메뉴에 따라 페이지 전환
if selected_option == "홈":
    st.session_state["page"] = "home"
    display_home()
elif selected_option == "도마뱀 분석":
    st.session_state["page"] = "image_analysis"
    display_image_analysis()
elif selected_option == "병원 검색":
    st.session_state["page"] = "hospital_page"
    display_hospitals(st.session_state.get("query", "파충류 동물병원"))
elif selected_option == "유튜브 검색":
    st.session_state["page"] = "youtube_page"
    display_youtube_videos(st.session_state.get("query", "파충류 사육"))
