import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import os
import keras
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from naver import search_hospitals
from youtube import search_youtube_videos

# ✅ 모델 및 데이터 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 실행 중인 디렉토리
MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(MODEL_DIR, "keras_model.h5")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.txt")

# ✅ `DepthwiseConv2D` 커스텀 클래스 등록
@keras.saving.register_keras_serializable()
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # `groups` 키 제거
        super().__init__(*args, **kwargs)

# ✅ 모델 불러오기 함수
def load_model_cached():
    try:
        if not os.path.exists(MODEL_PATH):
            st.error("❌ 모델 파일이 존재하지 않습니다. 올바른 경로인지 확인하세요.")
            return None
        custom_objects = {"DepthwiseConv2D": CustomDepthwiseConv2D}
        return load_model(MODEL_PATH, compile=False, custom_objects=custom_objects)
    except Exception as e:
        st.error(f"❌ 모델 로드 중 오류 발생: {e}")
        return None

# ✅ 레이블 불러오기
def load_labels():
    try:
        if not os.path.exists(LABELS_PATH):
            st.error("❌ 레이블 파일이 존재하지 않습니다.")
            return []
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        st.error(f"❌ 레이블 파일 로드 중 오류 발생: {e}")
        return []

# 🦎 도마뱀 품종 예측 함수
def predict_species(image, model, labels):
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    return labels[index], prediction[0][index]

# ✅ Streamlit UI 설정
st.set_page_config(page_title="도마뱀 품종 예측", layout="wide")

st.title("🦎 도마뱀 품종 예측")

# ✅ 모델 및 데이터 로드
model = load_model_cached()
labels = load_labels()

# 📂 파일 업로드 기능
uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)


    with st.spinner("🔍 이미지 분석 중..."):
        if model and labels:
            species, confidence = predict_species(image, model, labels)
            st.success(f"예측된 도마뱀 품종: **{species}**")
            st.write(f"✅ 신뢰도(Confidence): **{confidence:.2f}**")
        else:
            st.error("❌ 모델이 준비되지 않았습니다. 파일을 확인해주세요.")

# 🏥 병원 검색
st.sidebar.title("🏥 파충류 전문 병원 검색")
hospital_query = st.sidebar.text_input("검색어 입력", "파충류 동물병원")

if hospital_query:
    hospitals = search_hospitals(hospital_query)
    if hospitals:
        for hospital in hospitals:
            st.sidebar.markdown(f"### [{hospital['title']}]({hospital['link']})")
            st.sidebar.write(f"📍 주소: {hospital['address']}")
            st.sidebar.write(f"📞 전화번호: {hospital.get('telephone', '정보 없음')}")
    else:
        st.sidebar.write("❌ 검색 결과가 없습니다.")

# 📺 유튜브 영상 검색
st.sidebar.header("📺 파충류 관련 유튜브 영상")
youtube_query = st.sidebar.text_input("유튜브 검색어 입력", "파충류 사육")

if youtube_query:
    videos = search_youtube_videos(youtube_query)
    for video in videos:
        st.sidebar.markdown(f"### [{video['title']}]({video['link']})")
        st.sidebar.write(video["description"])
