import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import os
from tensorflow.keras.models import load_model # type: ignore

# 파일 경로 설정
MODEL_PATH = "./keras_model.h5"
LABELS_PATH = "./labels.txt"
CSV_PATH = "./Lizards.csv"

# 모델 불러오기
@st.cache_data
def load_model_cached():
    if not os.path.exists(MODEL_PATH):
    
        return None
    return load_model(MODEL_PATH, compile=False)

# 레이블 불러오기
def load_labels():
    if not os.path.exists(LABELS_PATH):
        return []
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

# CSV 데이터 불러오기
def load_csv():
    if not os.path.exists(CSV_PATH):
    
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)

# 예측 수행 함수
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

# 스트림릿 앱 시작
st.title("🦎 도마뱀 품종 및 대략적인 가격 확인")
st.write("이미지를 업로드하면 도마뱀 품종을 식별하고 대략적인 가격을 알려드립니다.")

# 모델 및 데이터 로드
model = load_model_cached()
labels = load_labels()
df = load_csv()

# 파일 업로드 기능
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드된 이미지', use_column_width=True)
        
        with st.spinner("이미지 분석 중..."):
            species, confidence = predict_species(image, model, labels)
            st.success(f"예측된 도마뱀 품종: **{species}**")
            st.write(f"✅ 신뢰도(Confidence): **{confidence:.2f}**")
            
            # 가격 정보 가져오기
            price_info = df[df['Species'] == species]['Price'].values
            if len(price_info) > 0:
                st.write(f"💰 예상 가격 범위: **{price_info[0]}**")
            else:
                st.write("❌ 해당 품종의 가격 정보를 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

st.write("업로드한 도마뱀의 품종과 가격 정보를 확인하세요! 🦎")
