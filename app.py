import os
import streamlit as st
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos
from about import show_about
from data_analysis import display_data_analysis
from image_analysis import display_image_analysis

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 이미지 파일 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 절대 경로
image_path = os.path.join(base_dir, "image", "home_image3.png")

# ✅ 사이드바 메뉴 렌더링
selected_option = render_sidebar()

# ✅ 기능 목록을 딕셔너리로 관리 (선택된 옵션에 따라 동적 변경)
feature_list = {
    "설명": [("📖 간단한 사용 설명서 (기본 기능 안내)", "#5F04B4")],
    "도마뱀 분석": [("🦎 도마뱀 이미지 분석 (품종 예측 기능)", "#FF9800")],
    "병원 검색": [("🏥 파충류 전문 병원 검색 (지역별 검색 지원)", "#03A9F4")],
    "유튜브 검색": [("🎥 파충류 관련 유튜브 영상 검색 (최신 정보 제공)", "#E91E63")],
    "분석 데이터": [("📊 데이터 분석 기능", "#795548")],
}

# ✅ 선택된 메뉴에 따라 기능 목록 동적 출력
st.markdown("<ul style='font-size:20px; color:#333; padding-left:20px;'>", unsafe_allow_html=True)
for feature, color in feature_list.get(selected_option, []):
    st.markdown(f"<li style='color:{color};'><b>{feature}</b></li>", unsafe_allow_html=True)
st.markdown("</ul>", unsafe_allow_html=True)

# ✅ 각 메뉴별 기능 실행
if selected_option == "설명":
    try:
        show_about()
    except Exception as e:
        st.error(f"❌ 설명 페이지 로드 오류: {e}")

elif selected_option == "도마뱀 분석":
    try:
        display_image_analysis()
    except Exception as e:
        st.error(f"❌ 도마뱀 분석 기능 오류: {e}")

elif selected_option == "병원 검색":
    try:
        display_hospitals()
    except Exception as e:
        st.error(f"❌ 병원 검색 기능 오류: {e}")

elif selected_option == "유튜브 검색":
    try:
        display_youtube_videos()
    except Exception as e:
        st.error(f"❌ 유튜브 검색 기능 오류: {e}")

elif selected_option == "분석 데이터":
    try:
        display_data_analysis()
    except Exception as e:
        st.error(f"❌ 데이터 분석 기능 오류: {e}")
