import streamlit as st
from image_analysis import BASE_DIR, display_image_analysis  # 올바른 모듈 import
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

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


# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 렌더링
if selected_option == "홈":
    st.title("🦎 파충류 검색 앱")
    st.write("이 앱은 도마뱀 이미지 분석, 병원 검색, 유튜브 검색 기능을 제공합니다.")
elif selected_option == "도마뱀 분석":
    display_image_analysis()

    

