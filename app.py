import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore
from sidebar import render_sidebar
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ 커스텀 레이어 정의 및 등록
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 키워드 제거
        super().__init__(*args, **kwargs)

get_custom_objects()["CustomDepthwiseConv2D"] = CustomDepthwiseConv2D

# ✅ 모델 및 레이블 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

# ✅ 모델 및 레이블 불러오기 함수
@st.cache_data
def load_model_cached():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error("❌ 모델 파일이 존재하지 않습니다.")
            return None
        return load_model(MODEL_PATH, compile=False, custom_objects={"CustomDepthwiseConv2D": CustomDepthwiseConv2D})
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

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

# ✅ 도마뱀 품종 예측 함수
def predict_species(image, model, labels):
    try:
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        return labels[index], prediction[0][index] * 100  # 신뢰도 (%)
    except Exception as e:
        st.error(f"❌ 이미지 예측 중 오류 발생: {e}")
        return "알 수 없음", 0

# ✅ 페이지 초기화
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# ✅ 홈 페이지 렌더링 함수
def display_home():
    st.title("🦎 파충류 정보 검색 앱")
    col1, col2 = st.columns([1, 2])

    with col1:
        image_path = os.path.join(BASE_DIR, "image", "001.jpg")
        if os.path.exists(image_path):
            st.image(image_path, width=200)
        else:
            st.error("❌ 홈 화면 이미지 파일이 없습니다.")

    with col2:
        st.write("""
        🦎 **앱 기능**
        - 도마뱀 이미지 분석
        - 파충류 전문 병원 검색
        - 파충류 관련 유튜브 영상 검색
        """)

def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")
    model = load_model_cached()
    labels = load_labels()

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", width=300)
        if model and labels:
            species, confidence = predict_species(image, model, labels)
            st.success(f"**예측된 도마뱀 품종: {species}**")
            st.write(f"✅ 신뢰도: **{confidence:.2f}%**")

# ✅ 사이드바 렌더링
selected_option = render_sidebar()

# ✅ 선택된 메뉴에 따라 페이지 전환
if selected_option == "홈":
    st.session_state["page"] = "home"
    display_home()
elif selected_option == "병원 검색":
    st.session_state["page"] = "hospital_page"
    display_hospitals(st.session_state.get("query", "파충류 동물병원"))
elif selected_option == "유튜브 검색":
    st.session_state["page"] = "youtube_page"
    display_youtube_videos(st.session_state.get("query", "파충류 사육"))
