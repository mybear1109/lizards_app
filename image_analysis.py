import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore
import h5py
from species_info import get_species_description
from data_manager import save_prediction

# ✅ DepthwiseConv2D 호환성 해결
class DepthwiseConv2DCompat(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)
        super().__init__(*args, **kwargs)

# ✅ 커스텀 레이어 등록
get_custom_objects()["DepthwiseConv2DCompat"] = DepthwiseConv2DCompat

# ✅ 모델 및 레이블 경로 설정
MODEL_PATH = "model/keras_model.h5"
LABELS_PATH = "model/labels.txt"

def load_model_cached():
    """ 모델을 불러오는 함수 """
    try:
        model = load_model(MODEL_PATH, compile=False, custom_objects={"DepthwiseConv2D": DepthwiseConv2DCompat})
        return model
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

def load_labels():
    """ 레이블 파일을 불러오는 함수 """
    try:
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        st.error(f"❌ 레이블 파일 로드 중 오류 발생: {e}")
        return []

# ✅ 도마뱀 품종 예측 함수
def predict_species(image, model, labels):
    """ 업로드된 이미지로 도마뱀 품종을 예측하는 함수 """
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
        st.error(f"❌ 이미지 예측 중 오류 발생: {e}")
        return "알 수 없음", 0

# ✅ 도마뱀 이미지 분석 기능
def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")

    # ✅ 모델 및 레이블 불러오기
    model = load_model_cached()
    labels = load_labels()

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

            # ✅ 모프 선택 기능 추가
            morph_options = [
                'White', 'Albino', 'Green', 'Undefined', 'Berry', 'Red', 'Normal',
                'Hypo', 'Lily', 'Frapuccino', 'Cappuccino', 'Stripe', 'Dark',
                'Spotless', 'Black', 'Dalmatian', 'Cream', 'Hat', 'Axanthic', 'Yellow'
            ]
            morph = st.selectbox("🦎 업로드한 도마뱀의 모프를 선택해주세요.", morph_options)
            st.info(f"🔍 선택한 모프: **{morph}** 입니다. 소중한 정보 감사합니다.")

            # ✅ 분석 데이터 저장 (모프 추가)
            save_prediction(uploaded_file.name, species, confidence, morph)

            # ✅ 품종 설명 표시
            display_species_info(species)

            # ✅ 주의 사항 안내
            st.info("""
                🔍 예측 결과는 입력된 이미지의 특성에 따라 변동될 수 있습니다.

                ⚠️ 이 결과는 참고용으로만 활용해 주시기 바랍니다.

                📝 실제 결과와 차이가 있을 수 있음을 양지해 주시기 바랍니다.
            """)

        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")

# ✅ 품종 설명 UI 표시 함수
def display_species_info(species_name):
    """ 도마뱀 품종 설명을 출력하는 함수 """
    species_info = get_species_description(species_name)  

    if not species_info:  
        species_info = {"설명": "정보 없음", "서식지": "정보 없음", "먹이": "정보 없음", "특징": "정보 없음"}  

    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            ">
            <h3 style="color: #4CAF50;">🦎 {species_name}</h3>
            <p><b>📝 설명:</b> {species_info['설명']}</p>
            <p><b>📍 서식지:</b> {species_info['서식지']}</p>
            <p><b>🍽️ 먹이:</b> {species_info['먹이']}</p>
            <p><b>✨ 특징:</b> {species_info['특징']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
