import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore
import h5py  # h5 파일 무결성 체크
from species_info import get_species_description

# ✅ 커스텀 레이어 정의 (DepthwiseConv2D 호환성 문제 해결)
class DepthwiseConv2DCompat(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 제거 (Keras 3.x 대비)
        super().__init__(*args, **kwargs)

# ✅ 커스텀 레이어 등록
get_custom_objects()["DepthwiseConv2DCompat"] = DepthwiseConv2DCompat

# ✅ 모델 및 레이블 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "keras_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.txt")

# ✅ 모델 존재 여부 확인 함수
def check_model_exists():
    if not os.path.exists(MODEL_PATH):
        st.error("❌ 모델 파일이 존재하지 않습니다. 올바른 경로를 확인하세요.")
        return False
    try:
        with h5py.File(MODEL_PATH, "r") as f:  # h5 파일 무결성 체크
            pass
        return True
    except Exception as e:
        st.error(f"❌ 모델 파일이 손상되었습니다. 다시 업로드하세요. 오류: {e}")
        return False

# ✅ 모델 및 레이블 불러오기 함수
@st.cache_data
def load_model_cached():
    if not check_model_exists():
        return None

    try:
        model = load_model(MODEL_PATH, compile=False, custom_objects={"DepthwiseConv2D": DepthwiseConv2DCompat})
        return model
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
            st.image(image, caption="업로드된 이미지", width=300)
            
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
            # 업로드된 이미지 표시
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)

            # ✅ 이미지 분석 실행
            species, confidence = predict_species(image, model, labels)
            st.success(f"**예측된 도마뱀 품종: {species}**")
            st.write(f"✅ 신뢰도: **{confidence:.2f}%**")

            # ✅ 품종 설명 출력
            description = get_species_description(species)
            if description:
                st.markdown(f"### 🦎 품종 설명")
                st.info(description)
            else:
                st.warning("해당 품종에 대한 추가 정보가 없습니다.")

            # 안내 메시지 출력
            st.markdown("""
            ---
            예측 결과는 입력된 이미지의 특성에 따라 변동될 수 있습니다.
            
            이 결과는 참고용으로만 활용해 주시기 바랍니다.
            
            실제 결과와 차이가 있을 수 있음을 양지해 주시기 바랍니다.
            """)

        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")

