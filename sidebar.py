import os
import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # ✅ 이미지 경로 설정
        image_path = "image/home_image.png"

        # ✅ 이미지 존재 여부 확인
        if not os.path.exists(image_path):
            st.warning(f"⚠️ 이미지 파일을 찾을 수 없습니다: `{image_path}`")
            image_path = None  # 이미지가 없을 경우 None으로 설정

        # ✅ 가운데 정렬된 이미지 표시 (파일이 있을 경우)
        if image_path:
            st.image(image_path, width=200)

            
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
