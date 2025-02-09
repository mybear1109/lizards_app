import os
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.utils import get_custom_objects # type: ignore
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

def display_image_analysis():
    st.subheader("🦎 도마뱀 이미지 분석")

    # ✅ 파일 업로드 (고유 키 사용)
    uploaded_file = st.file_uploader(
        "도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"], key="image_uploader_analysis"
    )

    # ✅ 모델 및 레이블 로드
    model = load_model_cached()
    labels = load_labels()

    if model is None or not labels:
        st.error("⚠️ 모델 또는 레이블 파일이 올바르게 로드되지 않았습니다.")
        return

    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # ✅ 컬럼을 이용한 정렬 (왼쪽: 이미지 / 오른쪽: 예측 결과 및 설명)
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(image, caption="업로드된 이미지", width=300)

            with col2:
                # ✅ 이미지 분석 실행
                species, confidence = predict_species(image, model, labels)

                # ✅ 예측 결과 강조 표시 (설명 위에 고정)
                st.markdown(
                    f"""
                    <div style="
                        background-color: #ffcc80; 
                        padding: 10px; 
                        border-radius: 10px;
                        text-align: center;
                        font-size: 20px;
                        font-weight: bold;
                        color: #333;
                    ">
                        🦎 예측 결과: <span style="color:#d84315;">{species}</span>  
                        <br> ✅ 신뢰도: <span style="color:#d84315;">{confidence:.2f}%</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ✅ 예측 결과에 대한 설명 표시
                species_info = get_species_description(species)


                # 설명, 서식지, 먹이를 온점으로 분리하여 HTML 형식으로 변환
                def split_by_period(text):
                    sentences = text.split('.')
                    return '<br>'.join([sentence.strip() + '.' for sentence in sentences if sentence.strip()])

                explanation_html = split_by_period(species_info["설명"])
                habitat_html = split_by_period(species_info["서식지"])
                food_html = split_by_period(species_info["먹이"])

                # 특징 문자열을 줄바꿈으로 분리하여 HTML 형식으로 변환
                features_html = "<br>".join(species_info["특징"].split("\n"))

                st.markdown(
                    f"""
                    <div style="
                        background-color: #f8f9fa; 
                        padding: 15px; 
                        border-radius: 10px;
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                        line-height: 1.6;  /* 줄 간격 조정 */
                    ">
                        <h3 style="color: #4CAF50; font-size: 24px; margin-bottom: 15px;">🦎 {species}</h3>
                        <p style="margin: 10px 0; font-size: 16px; color: #333;">
                            <b>📝 설명:</b><br>{explanation_html}
                        </p>
                        <p style="margin: 10px 0; font-size: 16px; color: #333;">
                            <b>📍 서식지:</b><br>{habitat_html}
                        </p>
                        <p style="margin: 10px 0; font-size: 16px; color: #333;">
                            <b>🍽️ 먹이:</b><br>{food_html}
                        </p>
                        <p style="margin: 10px 0; font-size: 16px; color: #333;">
                            <b>✨ 특징:</b><br>{features_html}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            st.write("")
            st.write("")
            # ✅ 추가 정보 입력 (하단 배치)
            st.subheader("📋 추가 정보 입력")
            st.write("🔍 예측 신뢰도를 변경하여 추가 정보를 입력 할 수 있습니다.")

            confidence = st.slider("예측 신뢰도", 0, 100, int(confidence))

            # ✅ 사용자가 직접 정보 입력 가능
            species_options = ["0 개구리(Frog)","1 거북이(Turtle)","2 기타(Other)", "3 뉴트(newt)",
                                "4 도롱뇽(Salamander)","5 두꺼비(Toad)","6 레오파드 게코(Leopardgeko)",
                                "7 뱀(Snake)","8 비어디 드래곤(Beardy)","9 앨리게이터(Alligator)",
                                "10 이구아나(Iguana)","11 카멜레온(Chameleon)","12 크레스티드 게코(Crestedgeko)",
                                "13 크로커다일(Crocodile)","14 팩맨(PacMan)"]
            species = st.selectbox("🐢 파충류의 종류를 선택해주세요.🐍", species_options)
            st.write("")
            size_options = ['성체(Adult)/대형(Large)', '성체(Adult)/중형(Medium)', '성체(Adult)/소형(Small)',
                            '아성체(Juvenile)/대형(Large)', '아성체(Juvenile)/중형(Medium)', '아성체(Juvenile)/소형(Small)',
                            '유체(Hatchling)/대형(Large)', '유체(Hatchling)/중형(Medium)','유체(Hatchling)/소형(Small)']
            size = st.selectbox("🐊 파충류의 사이즈를 선택해주세요.🦖", size_options)
            st.write("")
            # 크레스티드 게코나 레오파드 게코를 선택한 경우에만 모프 선택 옵션 표시
            if species in ["6 레오파드 게코(Leopardgeko)", "12 크레스티드 게코(Crestedgeko)"]:
                morph_options = [
                    'Normal(일반)', 'Albino(알비노)', 'Leucistic(루시스틱)', 'Melanistic(멜라니스틱)',
                    'Hypomelanistic(하이포멜라니스틱)', 'Axanthic(액산틱)', 'Anerythristic(아네리스리스틱)',
                    'Piebald(파이볼드)', 'Tiger(타이거)', 'Stripe(스트라이프)', 'Banded(밴디드)', 'Spotted(스팟티드)',
                    'Dalmatian(달마시안)', 'Blizzard(블리자드)', 'Patternless(무늬없음)', 'Translucent(반투명)',
                    'Paradox(패러독스)', 'Chimera(키메라)', 'Enigma(에니그마)', 'Designer(디자이너)', 'Wild Type(야생형)',
                    'Undefined(미정)'
                ]
                morph = st.selectbox("🦎 도마뱀의 모프를 선택해주세요.", morph_options)
            else:
                st.info("모프 선택은 크레스티드 게코와 레오파드 게코에만 적용됩니다.🦎")

            st.write("")
            st.info("소중한 정보 입력해주셔서 감사합니다.😊")
            st.write("")      
            # ✅ 결과 저장 버튼
            if st.button("결과 저장"):
                save_prediction(uploaded_file.name, species, confidence, morph, size) # type: ignore
                st.success("✅ 분석 결과가 저장되었습니다.")
            st.write("")
            st.write("")

            # ✅ 주의 사항 안내 (맨 하단)
            st.error("""
                🔍 예측 결과는 입력된 이미지의 특성에 따라 변동될 수 있습니다.

                ⚠️ 이 결과는 참고용으로만 활용해 주시기 바랍니다.

                📝 실제 결과와 차이가 있을 수 있음을 양지해 주시기 바랍니다.
            """)

        except Exception as e:
            st.error(f"❌ 이미지 처리 중 오류 발생: {e}")
