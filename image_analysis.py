import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore

# ✅ 커스텀 레이어 정의 및 등록
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 키워드 제거
        super().__init__(*args, **kwargs)

get_custom_objects()["CustomDepthwiseConv2D"] = CustomDepthwiseConv2D

# ✅ 전역 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

# ✅ 모델 및 레이블 불러오기 함수
@st.cache_data
def load_model_cached():
    try:
        # 모델 경로 존재 여부 확인
        if not os.path.exists(MODEL_PATH):
            st.error("❌ 모델 파일이 존재하지 않습니다.")
            return None
        
        # 모델 로드 시도
        model = load_model(MODEL_PATH, compile=False, custom_objects={"CustomDepthwiseConv2D": CustomDepthwiseConv2D})
        return model
    except Exception as e:
        # 오류 디버깅 출력
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        st.error(f"모델 경로: {MODEL_PATH}")
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

# ✅ 도마뱀 이미지 분석 기능
def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")
    model = load_model_cached()
    labels = load_labels()
    model = load_model("model/keras_model.h5", compile=False, custom_objects={"CustomDepthwiseConv2D": CustomDepthwiseConv2D})
    model.save("model/keras_model_fixed.h5")


    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)
            if model and labels:
                species, confidence = predict_species(image, model, labels)
                st.success(f"**예측된 도마뱀 품종: {species}**")
                st.write(f"✅ 신뢰도: **{confidence:.2f}%**")
            else:
                st.error("❌ 모델 또는 레이블이 준비되지 않았습니다.")
        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")
