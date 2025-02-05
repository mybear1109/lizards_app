import os
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from PIL import Image, ImageOps
from streamlit_option_menu import option_menu

# ✅ 스트림릿 페이지 설정
st.set_page_config(page_title="파충류 검색 앱", layout="wide")

# ✅ DepthwiseConv2D 커스텀 레이어 등록 (Keras 3.x 및 TensorFlow 최신 버전 대응)
class CustomDepthwiseConv2D(DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)  # 'groups' 키워드 제거
        super().__init__(*args, **kwargs)

# ✅ Keras에 커스텀 레이어 등록
tf.keras.utils.get_custom_objects()["CustomDepthwiseConv2D"] = CustomDepthwiseConv2D

# ✅ 모델 불러오기 함수 수정
def load_model_cached():
    try:
        model_path = "./model/keras_model.h5"
        if not os.path.exists(model_path):
            raise FileNotFoundError("❌ 모델 파일이 존재하지 않습니다.")
        
        # 🔹 커스텀 레이어 적용하여 모델 로드
        model = load_model(model_path, compile=False, custom_objects={"DepthwiseConv2D": CustomDepthwiseConv2D})
        return model
    except Exception as e:
        print(f"❌ 모델 로드 중 오류 발생: {e}")
        return None
# ✅ 레이블 불러오기 함수
@st.cache_data
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
    try:
        size = (224, 224)  # 모델 입력 크기 조정
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # 모델 입력 데이터 준비
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
        image_path = "./image/001.jpg"
        if os.path.exists(image_path):
            st.image(image_path, width=200)  # 크기 조정
        else:
            st.error("❌ 홈 화면 이미지 파일이 없습니다.")

    with col2:
        # 설명 텍스트 표시
        st.write("""
        이 앱은 다음 기능을 제공합니다:
        - 🦎 도마뱀 이미지 분석
        - 🏥 파충류 전문 병원 검색
        - 📺 파충류 관련 유튜브 영상 검색
        """)

# 📂 이미지 분석 기능
def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")
    model = load_model_cached()
    labels = load_labels()

    uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)  # 크기 조정

            with st.spinner("🔍 이미지 분석 중..."):
                if model and labels:
                    species, confidence = predict_species(image, model, labels)
                    st.success(f"예측된 도마뱀 품종: **{species}**")
                    st.write(f"✅ 신뢰도: **{confidence:.2f}%**")
                    st.info(f"신뢰도는 모델이 {species} 품종을 얼마나 정확히 예측했는지 나타냅니다.")
                else:
                    st.error("❌ 모델이 준비되지 않았습니다.")
        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")

# 📍 사이드바 탐색
with st.sidebar:
    # 사이드바 상단 이미지 추가
    st.image("image/home_image.png", width=200)

    # 옵션 메뉴 생성
    choose = option_menu(
        menu_title="앱 탐색",  # 메뉴 제목
        options=["홈으로", "병원 검색", "유튜브 검색"],  # 메뉴 항목
        icons=["house.svg", "stethoscope", "bag-heart.svg","caret-right-square.svg"],  # FontAwesome 아이콘
        menu_icon="icons",  # 상단 메뉴 아이콘
        default_index=0,  # 기본 선택 항목
        styles={
            "container": {"padding": "5px", "background-color": "#f8f9fa"},
            "icon": {"color": "green", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#4caf50", "color": "white"},
        },
    )

# 선택된 메뉴에 따라 페이지 전환
if choose == "홈으로":
    st.session_state['page'] = "home"
    display_home()
    display_image_analysis()

elif choose == "병원 검색":
    st.session_state['page'] = "hospital_page"
    st.header("🏥 병원 검색")
    hospital_query = st.text_input("🔍 병원 검색어 입력", "파충류 동물병원")
    if st.button("병원 검색"):
        st.success(f"'{hospital_query}' 검색을 시작합니다!")
        st.session_state['query'] = hospital_query

elif choose == "유튜브 검색":
    st.session_state['page'] = "youtube_page"
    st.header("📺 유튜브 검색")
    youtube_query = st.text_input("🔍 유튜브 검색어 입력", "파충류 사육")
    if st.button("유튜브 검색"):
        st.success(f"'{youtube_query}' 검색을 시작합니다!")
        st.session_state['query'] = youtube_query
