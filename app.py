import re
import streamlit as st
import requests
import urllib.parse
import os

# ✅ 앱 페이지 설정 (항상 최상단에 위치)
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 사이드바 렌더링 함수
def render_sidebar():
    st.sidebar.title("메뉴")
    return st.sidebar.radio(
        "탐색",
        options=["홈", "설명", "도마뱀 분석", "병원 검색", "유튜브 검색", "데이터 분석"]
    )

# ✅ 각 메뉴별 기능 (함수 임포트 또는 정의 확인 필요)
try:
    from hospital_page import display_hospitals
    from youtube_page import display_youtube_videos
    from about import show_about
    from data_analysis import display_data_analysis
    from image_analysis import display_image_analysis
except ImportError as e:
    st.error(f"❌ 모듈 로드 오류: {e}")

# ✅ 선택된 메뉴 실행
selected_option = render_sidebar()

if selected_option == "홈":
    col1, col2 = st.columns([1, 2])  # 이미지(1) : 텍스트(2) 비율 설정

    with col1:
        st.image("image/001.jpg", use_column_width=True)

    with col2:
        st.markdown(
            "<h1 style='color:#4CAF50; font-size:42px; font-weight:bold;'>🦎 파충류 탐험의 세계</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='color:#555; font-size:24px;'>🐍 파충류를 사랑하는 사람들을 위한 다양한 기능을 제공합니다.</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <ul style="font-size:20px; color:#333;">
                <li>📖 <b style="color:#5F04B4;">간단한 사용 설명서</b> (기본 기능 안내)</li>           
                <li>🦎 <b style="color:#FF9800;">도마뱀 이미지 분석</b> (품종 예측 기능)</li>
                <li>🏥 <b style="color:#03A9F4;">파충류 전문 병원 검색</b> (지역별 검색 지원)</li>
                <li>🎥 <b style="color:#E91E63;">파충류 관련 유튜브 영상 검색</b> (최신 정보 제공)</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )
elif selected_option == "설명":
    try:
        show_about()
    except Exception as e:
        st.error(f"❌ 설명 페이지 실행 오류: {e}")

elif selected_option == "도마뱀 분석":
    try:
        display_image_analysis()
    except Exception as e:
        st.error(f"❌ 도마뱀 분석 기능 실행 오류: {e}")

elif selected_option == "병원 검색":
    try:
        display_hospitals()
    except Exception as e:
        st.error(f"❌ 병원 검색 실행 오류: {e}")

elif selected_option == "유튜브 검색":
    try:
        display_youtube_videos()
    except Exception as e:
        st.error(f"❌ 유튜브 검색 기능 실행 오류: {e}")

elif selected_option == "데이터 분석":
    try:
        display_data_analysis()
    except Exception as e:
        st.error(f"❌ 데이터 분석 기능 실행 오류: {e}")
