import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # 사이드바 이미지 추가
        st.image("image/home_image.png", width=300)

        # ✅ 검색창 스타일 및 메뉴 생성
        selected_option = option_menu(
            menu_title="앱 탐색",  # 메뉴 제목
            options=["홈", "도마뱀 분석", "병원 검색", "유튜브 검색"],  # 메뉴 항목
            icons=["house-door", "camera", "geo-alt", "play-circle"],  # 아이콘
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

        # ✅ 병원 검색 기능
        if selected_option == "병원 검색":
            st.subheader("🔍 병원 검색")
            # 검색어 입력 시 자동으로 세션에 저장
            st.text_input(
                "검색어 입력", 
                placeholder="예: 파충류 동물병원", 
                key="hospital_query"  # 검색어를 세션 상태로 저장
            )

        # ✅ 유튜브 검색 기능
        elif selected_option == "유튜브 검색":
            st.subheader("📺 유튜브 검색")
            # 검색어 입력 시 자동으로 세션에 저장
            st.text_input(
                "검색어 입력", 
                placeholder="예: 파충류 사육 방법", 
                key="youtube_query"  # 검색어를 세션 상태로 저장
            )

        return selected_option
