import os
import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        # ✅ 이미지 파일 경로 설정
        image_path = "image/home_image.png"
        default_image = "default_image.jpg"  # 기본 이미지 (없을 경우 대비)

        # ✅ 이미지 파일 존재 여부 확인
        if not os.path.isfile(image_path):
            st.warning("⚠️ 이미지 파일이 존재하지 않습니다. 기본 이미지를 표시합니다.")
            image_path = default_image  # 기본 이미지 사용

            if not os.path.isfile(image_path):
                st.error("🚨 기본 이미지도 존재하지 않습니다. 파일을 확인해주세요.")
                image_path = None  # 이미지 표시 안 함

        # ✅ 이미지 가운데 정렬하여 표시 (st.image 사용)
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
            hospital_query = st.text_input("🔍 병원 검색", "파충류 동물병원", key="hospital_query")
        elif selected_option == "유튜브 검색":
            youtube_query = st.text_input("📺 유튜브 검색", "파충류 사육 방법", key="youtube_query")

    return selected_option
