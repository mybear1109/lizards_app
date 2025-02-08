import os
import streamlit as st
from streamlit_option_menu import option_menu  # 사이드바 네비게이션용

# ✅ Streamlit 페이지 설정 (최상단 배치)
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 외부 모듈 임포트
try:
    from sidebar import render_sidebar
    from hospital_page import display_hospitals
    from youtube_page import display_youtube_videos
    from about import show_about
    from data_analysis import display_data_analysis
    from image_analysis import display_image_analysis
except ImportError as e:
    st.error(f"❌ 모듈 로드 오류: {e}")
    st.stop()

# ✅ 이미지 파일 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 절대 경로
image_path = os.path.join(base_dir, "image", "home_image3.jpg")

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 전환
if selected_option == "홈":
    # ✅ 제목 및 기능 설명 출력
    st.markdown(
        """
        <h1 style="color:#4CAF50; font-size:42px; font-weight:bold; text-align:center;">🦎 파충류 탐험의 세계</h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h3 style="color:#555; font-size:24px; text-align:center;">🐍 파충류를 사랑하는 사람들을 위한 다양한 기능을 제공합니다.</h3>
        """,
        unsafe_allow_html=True,
    )

    # ✅ 이미지 파일이 존재하는 경우에만 표시
    if os.path.exists(image_path):
        st.image(image_path, caption="홈 화면 이미지", use_column_width=True)  # ✅ 자동 크기 조정
    else:
        st.warning(f"⚠️ 이미지 파일을 찾을 수 없습니다. 경로를 확인하세요: {image_path}")

    # ✅ 버튼을 눌렀을 때 해당 페이지로 이동하도록 설정
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📖 간단한 사용 설명서"):
            st.session_state["selected_page"] = "설명"

    with col2:
        if st.button("🦎 도마뱀 분석"):
            st.session_state["selected_page"] = "도마뱀 분석"

    with col3:
        if st.button("🏥 병원 검색"):
            st.session_state["selected_page"] = "병원 검색"

    col4, col5 = st.columns([1, 1])
    
    with col4:
        if st.button("🎥 유튜브 검색"):
            st.session_state["selected_page"] = "유튜브 검색"

    with col5:
        if st.button("📊 데이터 분석"):
            st.session_state["selected_page"] = "분석 데이터"

# ✅ 세션 상태를 확인하여 해당 페이지로 이동
if "selected_page" in st.session_state:
    selected_option = st.session_state["selected_page"]

# ✅ 각 메뉴별 기능 실행
if selected_option == "설명":
    try:
        show_about()
    except Exception as e:
        st.error(f"❌ 설명 페이지 로드 오류: {e}")

elif selected_option == "도마뱀 분석":
    try:
        display_image_analysis()
    except Exception as e:
        st.error(f"❌ 도마뱀 분석 기능 오류: {e}")

elif selected_option == "병원 검색":
    try:
        display_hospitals()
    except Exception as e:
        st.error(f"❌ 병원 검색 기능 오류: {e}")

elif selected_option == "유튜브 검색":
    try:
        display_youtube_videos()
    except Exception as e:
        st.error(f"❌ 유튜브 검색 기능 오류: {e}")

elif selected_option == "분석 데이터":
    try:
        display_data_analysis()
    except Exception as e:
        st.error(f"❌ 데이터 분석 기능 오류: {e}")
