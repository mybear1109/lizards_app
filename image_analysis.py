import os
from plot import plot_prediction_chart  # ✅ plot.py에서 시각화 함수 가져오기
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore
import h5py  # h5 파일 무결성 체크
from species_info import get_species_description
import matplotlib.pyplot as plt
from data_manager import save_prediction
from data_analysis import load_existing_data  # ✅ 올바른 위치에서 가져오기

# ✅ DepthwiseConv2D 호환성 해결 (Keras 3.x 대비)
class DepthwiseConv2DCompat(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  
        super().__init__(*args, **kwargs)

# ✅ 커스텀 레이어 등록
get_custom_objects()["DepthwiseConv2DCompat"] = DepthwiseConv2DCompat

# ✅ 모델 경로 설정
MODEL_PATH = "model/keras_model.h5"
LABELS_PATH = "model/labels.txt"

# ✅ 모델 및 레이블 불러오기 함수
@st.cache_data
def load_model_cached():
    try:
        model = load_model(MODEL_PATH, compile=False, custom_objects={"DepthwiseConv2D": DepthwiseConv2DCompat})
        return model
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

@st.cache_data
def load_labels():
    try:
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

    # 모델 및 레이블 불러오기
    model = load_model_cached()
    labels = load_labels()

    # 모델이 정상적으로 로드되지 않았으면 중단
    if model is None or not labels:
        st.error("⚠️ 분석을 실행할 수 없습니다. 모델 또는 레이블 파일이 올바르게 로드되지 않았습니다.")
        return

    # ✅ 이미지 업로드 기능
    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            if image.mode != "RGB":
                image = image.convert("RGB")
            st.image(image, caption="업로드된 이미지", width=300)

            # ✅ 이미지 분석 실행
            species, confidence = predict_species(image, model, labels)
            st.success(f"**예측된 도마뱀 품종: {species}**")
            st.write(f"✅ 신뢰도: **{confidence:.2f}%**")

            # ✅ 분석 데이터 저장
            save_prediction(uploaded_file.name, species, confidence)  # ✅ 저장 추가

            # ✅ 기존 데이터 확인
            st.markdown("### 📋 기존 분석 데이터")
            df = load_existing_data()
            st.dataframe(df)

            # ✅ 품종 설명 표시
            display_species_info(species) # type: ignore

            # ✅ 확률 차트 생성
            st.markdown("### 📊 예측 확률 분포")
            plot_prediction_chart(labels, [confidence / 100])  # ✅ 시각화 추가

            # ✅ 안내 메시지 추가
            st.info("""
                    🔍 예측 결과는 입력된 이미지의 특성에 따라 변동될 수 있습니다.

                    ⚠️ 이 결과는 참고용으로만 활용해 주시기 바랍니다.

                    📝 실제 결과와 차이가 있을 수 있음을 양지해 주시기 바랍니다.
                    """)

        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")
