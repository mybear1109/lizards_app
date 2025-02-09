import os
import streamlit as st
from streamlit_option_menu import option_menu  # 사이드바 네비게이션용

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 외부 모듈 임포트
try:
    from sidebar import render_sidebar  # ✅ 사이드바 추가
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
image_path = os.path.join(base_dir, "images", "home_image3.png")

# ✅ 버튼 클릭 시 즉시 페이지 이동 함수
def navigate_to(page_name):
    """ 세션 상태를 업데이트하고 새로고침 """
    st.session_state["selected_page"] = page_name
    st.experimental_rerun()  # ✅ 강제 새로고침 (streamlit 최신 버전 대응)

# ✅ 세션 상태 초기화
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "홈"

# ✅ 사이드바 렌더링 (네비게이션 메뉴 추가)
selected_option = render_sidebar()

# ✅ 사이드바에서 선택한 메뉴와 동기화
if selected_option != st.session_state["selected_page"]:
    st.session_state["selected_page"] = selected_option
    st.experimental_rerun()

# ✅ 선택된 메뉴에 따라 페이지 전환
if st.session_state["selected_page"] == "홈":
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
        st.image(image_path, caption="홈 화면 이미지", use_container_width=True)  # ✅ 최신 버전 적용
    else:
        st.warning(f"⚠️ 이미지 파일을 찾을 수 없습니다. 경로를 확인하세요: {image_path}")

    # ✅ 버튼을 한 줄에 배치하여 클릭 시 해당 페이지로 이동
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("📖 앱 사용 방법"):
            navigate_to("앱 사용 방법")

    with col2:
        if st.button("🦎 도마뱀 분석"):
            navigate_to("도마뱀 분석")

    with col3:
        if st.button("🏥 병원 검색"):
            navigate_to("병원 검색")

    with col4:
        if st.button("🎥 유튜브 검색"):
            navigate_to("유튜브 검색")

    with col5:
        if st.button("📊 데이터 분석"):
            navigate_to("분석 데이터")

# ✅ 각 메뉴별 기능 실행 (세션 상태를 기준으로 연동)
if st.session_state["selected_page"] == "앱 사용 방법":
    try:
        show_about()
    except Exception as e:
        st.error(f"❌ 앱 사용 방법 페이지 로드 오류: {e}")

elif st.session_state["selected_page"] == "도마뱀 분석":
    try:
        display_image_analysis()
    except Exception as e:
        st.error(f"❌ 도마뱀 분석 기능 오류: {e}")

elif st.session_state["selected_page"] == "병원 검색":
    try:
        display_hospitals()
    except Exception as e:
        st.error(f"❌ 병원 검색 기능 오류: {e}")

elif st.session_state["selected_page"] == "유튜브 검색":
    try:
        display_youtube_videos()
    except Exception as e:
        st.error(f"❌ 유튜브 검색 기능 오류: {e}")

elif st.session_state["selected_page"] == "분석 데이터":
    try:
        display_data_analysis()
    except Exception as e:
        st.error(f"❌ 데이터 분석 기능 오류: {e}")
