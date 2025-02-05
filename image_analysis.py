import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects
from species_info import get_species_description

# ✅ 커스텀 DepthwiseConv2D 정의
class DepthwiseConv2DCompat(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 키워드 제거
        super().__init__(*args, **kwargs)

get_custom_objects()["DepthwiseConv2DCompat"] = DepthwiseConv2DCompat

# ✅ 모델 및 레이블 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

@st.cache_data
def load_model_cached():
    if not os.path.exists(MODEL_PATH):
        st.error("❌ 모델 파일이 존재하지 않습니다.")
        return None
    try:
        return load_model(MODEL_PATH, compile=False, custom_objects={"DepthwiseConv2DCompat": DepthwiseConv2DCompat})
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

@st.cache_data
def load_labels():
    if not os.path.exists(LABELS_PATH):
        st.error(f"❌ 레이블 파일이 존재하지 않습니다: {LABELS_PATH}")
        return []
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

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
        return labels[index], prediction[0][index] * 100
    except Exception as e:
        st.error(f"❌ 예측 중 오류 발생: {e}")
        return "알 수 없음", 0

def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")

    model = load_model_cached()
    labels = load_labels()

    if not model or not labels:
        st.error("⚠️ 모델 또는 레이블이 로드되지 않았습니다.")
        return

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)
            species, confidence = predict_species(image, model, labels)
            st.success(f"**예측된 도마뱀 품종: {species}**")
            st.write(f"✅ 신뢰도: **{confidence:.2f}%**")

            # ✅ 품종 설명 추가
            description = get_species_description(species)
            st.markdown("### 품종 설명")
            st.info(description)

        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")
