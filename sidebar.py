import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.image("image/home_image.png", width=200)

        # ✅ 메뉴 생성
        selected_option = option_menu(
            menu_title="앱 탐색",
            options=["홈", "도마뱀 분석", "병원 검색", "유튜브 검색"],
            icons=["house", "image", "hospital", "youtube"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#4caf50", "color": "white"},
            },
        )
    return selected_option
