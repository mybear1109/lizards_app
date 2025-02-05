import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    """
    사이드바 렌더링 함수
    """
    with st.sidebar:
        # 사이드바 상단 이미지 추가
        st.image("image/home_image.png", width=300)

        # ✅ 검색창 스타일 변경 (CSS 적용)
        st.markdown(
            "<style>"
            "input {font-size: 16px !important; font-family: Arial, sans-serif;}"
            "</style>",
            unsafe_allow_html=True,
        )

        # ✅ 메뉴 생성
        selected_option = option_menu(
            menu_title="앱 탐색",  # 메뉴 제목
            options=["홈", "도마뱀 분석", "병원 검색", "유튜브 검색"],  # 메뉴 항목
            icons=["house-door", "camera", "geo-alt", "play-circle"],  # 아이콘 변경
            menu_icon="menu-button",  # 상단 메뉴 아이콘
            default_index=0,  # 기본 선택 항목
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#4caf50", "color": "white"},
            },
        )

        # 병원 검색 기능 추가
        if selected_option == "병원 검색":
            st.subheader("🔍 병원 검색")
            hospital_query = st.text_input("검색어 입력", placeholder="예: 파충류 동물병원")
            st.session_state["hospital_query"] = hospital_query.strip()  # 세션 상태에 검색어 저장

    return selected_option
