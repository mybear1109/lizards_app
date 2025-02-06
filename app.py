import streamlit as st
from about import show_about
from image_analysis import display_image_analysis
from hospital_search import search_hospitals # type: ignore
from youtube_search import search_youtube # type: ignore

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="파충류 탐험의 세계", layout="wide")

# ✅ 사이드바 메뉴
st.sidebar.title("📌 탐험 메뉴")
page = st.sidebar.radio(
    "이동할 페이지를 선택하세요",
    ["홈", "이미지 분석", "병원 검색", "유튜브 검색"]
)

# ✅ 선택된 페이지 실행
if page == "홈":
    # ✅ 컬럼을 이용해 이미지와 텍스트 정렬
    col1, col2 = st.columns([1, 2])  # 이미지(1) : 텍스트(2) 비율 설정

    with col1:
        st.image("image/001.jpg", use_column_width=True)  # 이미지 추가 (경로 필요에 맞게 변경)

    with col2:
        # ✅ 제목 및 스타일 적용
        st.markdown(
            """
            <h1 style="color:#4CAF50; font-size:42px; font-weight:bold;">🦎 파충류 탐험의 세계</h1>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <h3 style="color:#555; font-size:24px;">🐍 파충류를 사랑하는 사람들을 위한 다양한 기능을 제공합니다.</h3>
            """,
            unsafe_allow_html=True,
        )

        # ✅ 기능 목록 (아이콘 및 스타일 적용)
        st.markdown(
            """
            <ul style="font-size:20px; color:#333;">
                <li>📸 <b style="color:#FF9800;">도마뱀 이미지 분석</b> (AI 기반 품종 예측 기능)</li>
                <li>🏥 <b style="color:#03A9F4;">파충류 전문 병원 검색</b> (위치 기반 검색 지원)</li>
                <li>🎥 <b style="color:#E91E63;">파충류 관련 유튜브 영상 검색</b> (최신 정보 제공)</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

    # ✅ 'about.py'에서 불러온 소개 페이지 추가
    show_about()

elif page == "이미지 분석":
    display_image_analysis()

elif page == "병원 검색":
    search_hospitals()

elif page == "유튜브 검색":
    search_youtube()
