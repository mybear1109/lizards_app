import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # ✅ 이미지 표시 (수정된 부분)
        st.image("image/home_image.png", width=200, caption="홈 이미지")

        # ✅ 네비게이션 메뉴 생성
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
                    "margin": "5px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#4caf50", "color": "white"},
            },
        )

        # ✅ 검색창 (선택된 메뉴에 따라 표시)
        if selected_option == "병원 검색":
            st.session_state["hospital_query"] = st.text_input("🔍 병원 검색", st.session_state.get("hospital_query", "파충류 동물병원"))
        elif selected_option == "유튜브 검색":
            st.session_state["youtube_query"] = st.text_input("📺 유튜브 검색", st.session_state.get("youtube_query", "파충류 사육 방법"))

    return selected_option
