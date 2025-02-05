import os
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from PIL import Image, ImageOps
from hospital_page import display_hospitals
from youtube_page import display_youtube_videos

# ✅ 스트림릿 페이지 설정 (반드시 코드 최상단에 위치)
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ DepthwiseConv2D 커스텀 레이어 등록 (TensorFlow 2.18 / Keras 3.x 대응)
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 파라미터 제거
        super().__init__(*args, **kwargs)

# Keras에 사용자 정의 레이어 등록
keras.utils.get_custom_objects()["CustomDepthwiseConv2D"] = CustomDepthwiseConv2D

# ✅ 모델 및 레이블 경로 설정
MODEL_PATH = "./model/keras_model.h5"
LABELS_PATH = "./model/labels.txt"

# ✅ 모델 불러오기 함수
@st.cache_data
def load_model_cached():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error("❌ 모델 파일이 존재하지 않습니다. 경로를 확인하세요.")
            return None
        return load_model(
            MODEL_PATH, 
            compile=False, 
            custom_objects={"DepthwiseConv2D": CustomDepthwiseConv2D}
        )
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

# ✅ 레이블 불러오기 함수
@st.cache_data
def load_labels():
    try:
        if not os.path.exists(LABELS_PATH):
            st.error("❌ 레이블 파일이 존재하지 않습니다. 경로를 확인하세요.")
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

        # 모델의 예상 입력 크기에 맞게 데이터 배열 생성
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
    st.session_state['page'] = "home"  # 초기 상태를 'home'으로 설정

# 🏠 홈 화면 UI
def display_home():
    st.title("🦎 파충류 정보 검색 앱")
    col1, col2 = st.columns([1, 2])  # 첫 번째 열이 좁고, 두 번째 열이 넓음

    with col1:
        # 이미지 파일 경로 설정
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "image", "001.jpg")

        st.write(f"디버깅: 이미지 경로 - {image_path}")  # 경로 디버깅 로그
        if os.path.exists(image_path):
            st.image(image_path, width=300, use_container_width=True)  # 홈 화면 이미지
        else:
            st.error("❌ 홈 화면 이미지 파일이 없습니다. 경로를 확인하세요.")

    with col2:
        # 텍스트 표시
        st.write("""
        이 앱은 다음 기능을 제공합니다:
        - 🦎 도마뱀 이미지 업로드 후 분석
        - 🏥 파충류 전문 병원 검색
        - 📺 파충류 관련 유튜브 영상 검색
        """)

# ✅ 페이지 전환 로직
if st.session_state['page'] == "home":
    display_home()
elif st.session_state['page'] == "hospital_page":
    display_hospitals(st.session_state.get('query', "파충류 동물병원"))
elif st.session_state['page'] == "youtube_page":
    display_youtube_videos(st.session_state.get('query', "파충류 사육"))

# 📂 이미지 분석 기능
if st.session_state['page'] == "home":
    st.subheader("🦎 도마뱀 이미지 분석")
    model = load_model_cached()
    labels = load_labels()

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_container_width=True)

            with st.spinner("🔍 이미지 분석 중..."):
                if model and labels:
                    species, confidence = predict_species(image, model, labels)
                    st.success(f"예측된 도마뱀 품종: **{species}**")
                    st.write(f"✅ 신뢰도: **{confidence:.2f} %**")
                else:
                    st.error("❌ 모델이 준비되지 않았습니다. 파일을 확인해주세요.")
        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")

# 📍 사이드바 탐색
st.sidebar.title("📍 탐색")
if st.sidebar.button("🏠 홈으로"):
    st.session_state['page'] = "home"

st.sidebar.header("🏥 병원 검색")
hospital_query = st.sidebar.text_input("병원 검색어 입력", "파충류 동물병원")
if st.sidebar.button("병원 검색"):
    st.session_state['query'] = hospital_query
    st.session_state['page'] = "hospital_page"

st.sidebar.header("📺 유튜브 검색")
youtube_query = st.sidebar.text_input("유튜브 검색어 입력", "파충류 사육")
if st.sidebar.button("유튜브 검색"):
    st.session_state['query'] = youtube_query
    st.session_state['page'] = "youtube_page"
