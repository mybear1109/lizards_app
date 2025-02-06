import os
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from data_manager import save_prediction  # ✅ 데이터 저장 모듈 사용
from data_analysis import load_existing_data  # ✅ 기존 데이터 불러오기
import matplotlib.pyplot as plt

# ✅ 모델 및 레이블 설정
MODEL_PATH = "model/keras_model.h5"
LABELS_PATH = "model/labels.txt"

# ✅ 모델 불러오기
@st.cache_data
def load_model_cached():
    """ 모델을 로드하고 캐싱하여 속도 향상 """
    try:
        model = load_model(MODEL_PATH, compile=False)
        return model
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

@st.cache_data
def load_labels():
    """ 레이블을 불러오는 함수 """
    try:
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        st.error(f"❌ 레이블 파일 로드 중 오류 발생: {e}")
        return []

def predict_species(image, model, labels):
    """ 이미지를 분석하고 예측된 종과 신뢰도를 반환 """
    try:
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        predictions = model.predict(data)[0]
        top_index = np.argmax(predictions)
        return labels[top_index], predictions[top_index] * 100, predictions
    except Exception as e:
        st.error(f"❌ 이미지 예측 중 오류 발생: {e}")
        return "알 수 없음", 0, None

def display_image_analysis():
    """ 도마뱀 이미지 분석 UI 표시 """
    st.subheader("🦎 도마뱀 이미지 분석")

    model = load_model_cached()
    labels = load_labels()

    if model is None or not labels:
        st.error("⚠️ 모델 또는 레이블 파일을 불러올 수 없습니다.")
        return

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        st.image(image, caption="업로드된 이미지", width=300)

        # ✅ 예측 실행
        species, confidence, predictions = predict_species(image, model, labels)
        st.success(f"**예측된 도마뱀 품종: {species}**")
        st.write(f"✅ 신뢰도: **{confidence:.2f}%**")

        # ✅ 분석 데이터 저장
        save_prediction(uploaded_file.name, species, confidence)

        # ✅ 기존 데이터 확인
        st.markdown("### 📋 기존 분석 데이터")
        df = load_existing_data()
        st.dataframe(df)

        # ✅ 확률 차트 생성
        st.markdown("### 📊 예측 확률 분포")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(labels, predictions * 100, color="skyblue")
        ax.set_xlabel("확률 (%)", fontsize=12)
        ax.set_ylabel("품종", fontsize=12)
        ax.set_title("품종별 예측 확률", fontsize=16)
        ax.set_xlim(0, 100)
        for i, v in enumerate(predictions * 100):
            ax.text(v + 1, i, f"{v:.1f}%", color="blue", va="center", fontsize=10)
        st.pyplot(fig)
