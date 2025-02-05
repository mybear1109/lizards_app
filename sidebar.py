import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    """
    사이드바를 렌더링하는 함수
    """
    with st.sidebar:  # 사이드바 컨텍스트 내에서 렌더링
        # 사이드바 상단 이미지 추가
        st.image("image/001.png", width=200)

        # ✅ 메뉴 생성
        selected_option = option_menu(
            menu_title="앱 탐색",  # 메뉴 제목
            options=["홈", "병원 검색", "유튜브 검색"],  # 메뉴 항목
            icons=["house", "hospital", "youtube"],  # FontAwesome 아이콘
            menu_icon="cast",  # 상단 메뉴 아이콘
            default_index=0,  # 기본 선택 항목
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
