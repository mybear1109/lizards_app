import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # 사이드바 이미지 추가
        st.image("image/home_image.png", width=300)

        # ✅ 검색창 스타일 및 메뉴 생성
        selected_option = option_menu(
            menu_title="앱 탐색",
            options=["홈", "설명", "도마뱀 분석", "병원 검색", "유튜브 검색"],
            icons=["house-door", "text", "camera", "geo-alt", "play-circle"],
            menu_icon="menu-button",
            default_index=0,
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

        # ✅ 병원 검색창
        if selected_option == "병원 검색":
            hospital_query = st.text_input("🔍 병원 검색", "파충류 동물병원", key="hospital_query")

        # ✅ 유튜브 검색창
        elif selected_option == "유튜브 검색":
            youtube_query = st.text_input("📺 유튜브 검색", "파충류 사육 방법", key="youtube_query")

    return selected_option
