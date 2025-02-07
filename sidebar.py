import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # 사이드바 이미지 추가
        st.image("image/home_image.png", width=200)
        # ✅ 가운데 정렬을 위한 HTML & CSS 적용
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <img src="image/home_image.png" width="200">
            </div>
            """,
            unsafe_allow_html=True,
        )
        # ✅ 검색창 스타일 및 메뉴 생성
        selected_option = option_menu(
            menu_title="🔍 탐색 메뉴",
            options=["홈", "설명", "도마뱀 분석", "병원 검색", "유튜브 검색", "분석 데이터"],
            icons=["house-door", "info-circle", "camera", "geo-alt", "play-circle", "bar-chart-line"],
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
