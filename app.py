import os
import streamlit as st
from streamlit_option_menu import option_menu  # 사이드바 네비게이션용

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="🦎 파충류 탐험 앱", layout="wide")

# ✅ 이미지 파일 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 절대 경로
home_image_path = os.path.join(base_dir, "images", "home_image3.png")
icon_image_path = os.path.join(base_dir, "images", "icon.png")

# ✅ 사이드바 네비게이션 메뉴 렌더링
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="images/icon.png" alt="icon" width="150" style="border-radius: 50%;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_option = option_menu(
        menu_title="🔍 탐색 메뉴",
        options=["홈", "설명", "도마뱀 분석", "병원 검색", "유튜브 검색", "데이터 분석"],
        icons=["house", "info-circle", "camera", "hospital", "youtube", "bar-chart"],
        menu_icon="list",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#f0f0f0"},
            "icon": {"font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "margin": "5px",
                "--hover-color": "#c1e1c5",
            },
            "nav-link-selected": {"background-color": "#4caf50", "color": "white"},
        },
    )

# ✅ 페이지별 콘텐츠 로드
if selected_option == "홈":
    # 메인 이미지 표시
    if os.path.exists(home_image_path):
        st.image(home_image_path, caption="🐍 파충류 탐험의 세계", use_container_width=True)
    else:
        st.warning("⚠️ 이미지 파일을 찾을 수 없습니다.")

    # 제목과 설명 추가
    st.markdown(
        """
        <h1 style="color:#4CAF50; text-align:center;">🦎 파충류 탐험의 세계에 오신 것을 환영합니다!</h1>
        <p style="font-size:18px; text-align:center;">
            🐍 파충류를 사랑하는 여러분을 위한<br>최고의 웹 애플리케이션!
        </p>
        """,
        unsafe_allow_html=True,
    )

    # 버튼으로 페이지 이동
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("📖 앱 사용 방법"):
            st.session_state["selected_page"] = "설명"

    with col2:
        if st.button("🦎 도마뱀 분석"):
            st.session_state["selected_page"] = "도마뱀 분석"

    with col3:
        if st.button("🏥 병원 검색"):
            st.session_state["selected_page"] = "병원 검색"

    with col4:
        if st.button("🎥 유튜브 검색"):
            st.session_state["selected_page"] = "유튜브 검색"

    with col5:
        if st.button("📊 데이터 분석"):
            st.session_state["selected_page"] = "데이터 분석"

elif selected_option == "설명":
    st.title("📖 간단한 사용 설명서")
    st.write("앱에 대한 설명과 주요 기능을 확인하세요.")

elif selected_option == "도마뱀 분석":
    st.title("🦎 도마뱀 이미지 분석")
    st.write("AI 모델을 이용한 도마뱀 이미지 분석 페이지입니다.")

elif selected_option == "병원 검색":
    st.title("🏥 파충류 전문 병원 검색")
    st.write("파충류 전문 병원을 검색할 수 있습니다.")

elif selected_option == "유튜브 검색":
    st.title("🎥 파충류 관련 유튜브 검색")
    st.write("파충류 관련 영상을 유튜브에서 검색하세요.")

elif selected_option == "데이터 분석":
    st.title("📊 데이터 분석")
    st.write("파충류 데이터를 분석하는 페이지입니다.")
