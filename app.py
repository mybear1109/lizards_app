import streamlit as st

# ✅ Streamlit 페이지 설정 (스크립트의 가장 첫 번째 명령으로 실행)
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 다른 모듈 import (이제 안전하게 실행됨)
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos
from about import show_about  # type: ignore
from data_analysis import display_data_analysis
from image_analysis import display_image_analysis  # ✅ `st.set_page_config()` 제거된 상태에서 import 가능

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 전환
if selected_option == "홈":
    col1, col2 = st.columns([1, 2])  # 이미지(1) : 텍스트(2) 비율 설정

    with col1:
        st.image("image/001.jpg", use_column_width=True)  # ✅ 이미지 추가

    with col2:
        st.markdown(
            """
            <h1 style="color:#4CAF50; font-size:42px; font-weight:bold;">🦎 파충류 탐험의 세계</h1>
            <h3 style="color:#555; font-size:24px;">🐍 파충류를 사랑하는 사람들을 위한 다양한 기능을 제공합니다.</h3>
            """,
            unsafe_allow_html=True,
        )

        # ✅ 기능 목록
        st.markdown(
            """
            <ul style="font-size:20px; color:#333;">
                <li>📖 <b>간단한 사용 설명서</b></li>           
                <li>🦎 <b>도마뱀 이미지 분석</b> (품종 예측 기능)</li>
                <li>🏥 <b>파충류 전문 병원 검색</b> (지역별 검색 지원)</li>
                <li>🎥 <b>파충류 관련 유튜브 영상 검색</b> (최신 정보 제공)</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

elif selected_option == "설명":
    show_about()
elif selected_option == "도마뱀 분석":
    display_image_analysis()  # ✅ `st.set_page_config()` 제거된 `image_analysis.py`에서 실행됨
elif selected_option == "병원 검색":
    display_hospitals()
elif selected_option == "유튜브 검색":
    display_youtube_videos()
elif selected_option == "데이터 분석":
    display_data_analysis()  # type: ignore
