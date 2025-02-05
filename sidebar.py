import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    """
    사이드바를 렌더링하는 함수
    """
    # 사이드바 상단 이미지 추가
    st.image("image/home_image.png", width=200)

    # ✅ 로컬 SVG 아이콘 파일 경로 설정
    icons_path = {
        "홈": "icons/house.svg",
        "병원 검색": "icons/bag-heart.svg",
        "유튜브 검색": "icons/caret-right-square.svg",
    }

    # ✅ HTML을 사용하여 아이콘 삽입
    def get_icon_html(icon_path):
        """아이콘을 HTML로 변환하는 함수"""
        return f'<img src="{icon_path}" width="20" style="margin-right:10px">'

    # ✅ 옵션 메뉴 생성
    choose = option_menu(
        menu_title="앱 탐색",
        options=["홈", "병원 검색", "유튜브 검색"],
        icons=[
            get_icon_html(icons_path["홈"]),
            get_icon_html(icons_path["병원 검색"]),
            get_icon_html(icons_path["유튜브 검색"]),
        ],
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
    return choose
