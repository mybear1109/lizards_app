import os
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from PIL import Image, ImageOps
from streamlit_option_menu import option_menu
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ DepthwiseConv2D 커스텀 레이어 등록 (Keras 3.x 및 TensorFlow 최신 버전 대응)
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 키워드 제거
        super().__init__(*args, **kwargs)

# ✅ Keras에 커스텀 레이어 등록
tf.keras.utils.get_custom_objects()["CustomDepthwiseConv2D"] = CustomDepthwiseConv2D

# ✅ 모델 및 레이블 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

# ✅ 모델 불러오기 함수
@st.cache_data
def load_model_cached():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error("❌ 모델 파일이 존재하지 않습니다.")
            return None
        return load_model(
            MODEL_PATH, compile=False, custom_objects={"CustomDepthwiseConv2D": CustomDepthwiseConv2D}
        )
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

# ✅ 레이블 불러오기 함수
@st.cache_data
def load_labels():
    try:
        if not os.path.exists(LABELS_PATH):
            st.error(f"❌ 레이블 파일이 존재하지 않습니다: {LABELS_PATH}")
            return []
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        st.error(f"❌ 레이블 파일 로드 중 오류 발생: {e}")
        return []

# 🦎 도마뱀 품종 예측 함수
def predict_species(image, model, labels):
    try:
        size = (224, 224)  # 모델 입력 크기 조정
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # 모델 입력 데이터 준비
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # 예측 실행
        prediction = model.predict(data)
        index = np.argmax(prediction)

        return labels[index], prediction[0][index] * 100  # 신뢰도를 %로 변환
    except Exception as e:
        st.error(f"❌ 이미지 예측 중 오류 발생: {e}")
        return "알 수 없음", 0

# ✅ 페이지 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = "home"

# 🏠 홈 화면 UI
def display_home():
    st.title("🦎 파충류 정보 검색 앱")
    col1, col2 = st.columns([1, 2])

    with col1:
        # 이미지 파일 경로 설정
        image_path = os.path.join(BASE_DIR, "image", "001.jpg")
        if os.path.exists(image_path):
            st.image(image_path, width=200)  # 크기 조정
        else:
            st.error("❌ 홈 화면 이미지 파일이 없습니다.")

    with col2:
        st.write("""
        🦎 **앱 기능**
        - 도마뱀 이미지 분석
        - 파충류 전문 병원 검색
        - 파충류 관련 유튜브 영상 검색
        """)

# 📂 이미지 분석 기능
def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")
    model = load_model_cached()
    labels = load_labels()

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)

            with st.spinner("🔍 이미지 분석 중..."):
                if model and labels:
                    species, confidence = predict_species(image, model, labels)
                    st.success(f"**예측된 도마뱀 품종: {species}**")
                    st.write(f"✅ 신뢰도: **{confidence:.2f}%**")
                    st.info(f"신뢰도는 모델이 {species} 품종을 얼마나 정확히 예측했는지 나타냅니다.")
                else:
                    st.error("❌ 모델이 준비되지 않았습니다.")
        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")

# 📍 사이드바 탐색
with st.sidebar:
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

    # ✅ 옵션 메뉴 생성 (아이콘을 HTML로 삽입)
    choose = option_menu(
        menu_title="앱 탐색",
        options=["홈", "병원 검색", "유튜브 검색"],
        icons=[get_icon_html(icons_path["홈"]), get_icon_html(icons_path["병원 검색"]), get_icon_html(icons_path["유튜브 검색"])],
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

# ✅ 선택된 메뉴에 따라 페이지 전환
if choose == "홈":
    st.session_state['page'] = "home"
    st.title("🦎 파충류 정보 검색 앱")
elif choose == "병원 검색":
    st.session_state['page'] = "hospital_page"
    st.header("🏥 병원 검색")
    hospital_query = st.text_input("🔍 병원 검색어 입력", "파충류 동물병원")
    if st.button("병원 검색"):
        st.success(f"'{hospital_query}' 검색을 시작합니다!")
        st.session_state['query'] = hospital_query
elif choose == "유튜브 검색":
    st.session_state['page'] = "youtube_page"
    st.header("📺 유튜브 검색")
    youtube_query = st.text_input("🔍 유튜브 검색어 입력", "파충류 사육")
    if st.button("유튜브 검색"):
        st.success(f"'{youtube_query}' 검색을 시작합니다!")
        st.session_state['query'] = youtube_query