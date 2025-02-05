import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.image("image/home_image.png", width=300)

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

        # ✅ 검색 기능 추가
        if selected_option == "병원 검색":
            st.subheader("🔍 병원 검색")
            hospital_query = st.text_input("검색어를 입력하세요", placeholder="예: 파충류 동물병원")

            if st.button("검색 실행"):
                st.session_state["query"] = hospital_query  # 검색어 저장
                st.success(f"'{hospital_query}' 검색을 실행합니다.")

        elif selected_option == "유튜브 검색":
            st.subheader("📺 유튜브 검색")
            youtube_query = st.text_input("검색어를 입력하세요", placeholder="예: 파충류 사육 방법")

            if st.button("검색 실행"):
                st.session_state["query"] = youtube_query  # 검색어 저장
                st.success(f"'{youtube_query}' 검색을 실행합니다.")

    return selected_option
