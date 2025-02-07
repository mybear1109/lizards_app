import os
import pandas as pd
import datetime
from PIL import Image
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"

# ✅ CSV 파일의 올바른 컬럼 구조 (Morph 및 Price 컬럼 포함)
EXPECTED_COLUMNS = ["Date", "Image", "Size", "Species", "Confidence", "Morph", "Price"]

# ✅ 이미지 저장 함수
def save_image(image_file):
    """ 이미지를 'data/images/' 폴더에 저장하는 함수 """
    try:
        # 저장할 파일 경로 생성 (유니크한 이름 부여)
        if hasattr(image_file, "name"):
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
        else:
            image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file}"

        # 저장할 디렉토리가 없으면 생성
        os.makedirs(IMAGE_FOLDER, exist_ok=True)

        # 이미지 파일 저장 경로
        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # 이미지 열기
        image = Image.open(image_file)

        # 파일 형식 확인 (지원되는 이미지 형식인지)
        if image.format not in ['JPEG', 'PNG']:
            st.error("❌ 지원되지 않는 이미지 형식입니다. JPG 또는 PNG 파일을 업로드해주세요.")
            return None

        # 이미지를 지정된 경로에 저장
        image.save(image_path)
        st.success(f"✅ 이미지가 성공적으로 저장되었습니다: {image_path}")
        return image_path, image_name  # 이미지 경로와 이름 반환

    except Exception as e:
        st.error(f"❌ 이미지 저장 중 오류 발생: {e}")
        return None, None

# ✅ 데이터 CSV 저장 함수
def save_prediction(image_file, species, confidence, morph="", size="", price=""):
    """ 분석된 결과를 CSV 파일에 추가하는 함수 """
    try:
        # ✅ 이미지 파일 저장
        image_path, image_name = save_image(image_file)
        if image_path is None:
            return  # 이미지 저장 실패 시 종료

        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # ✅ 새로운 데이터 생성 (기본값 자동 적용)
        new_data = pd.DataFrame([{
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Image": image_name,
            "Size": size,
            "Species": species,
            "Confidence": confidence,
            "Morph": morph,
            "Price": price
        }])

        # ✅ 기존 데이터 로드 및 컬럼 정리
        if os.path.exists(DATA_PATH):
            try:
                existing_data = pd.read_csv(DATA_PATH, encoding="utf-8-sig", on_bad_lines="skip")

                # ✅ 기존 컬럼 체크 및 자동 수정
                for col in EXPECTED_COLUMNS:
                    if col not in existing_data.columns:
                        existing_data[col] = ""

                existing_data = existing_data[EXPECTED_COLUMNS]  # ✅ 컬럼 정렬
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                st.success("✅ 기존 데이터 로드 및 병합 완료")

            except Exception as e:
                st.error(f"❌ 기존 데이터 읽기 오류: {e}")
                updated_data = new_data  # 기존 데이터가 깨진 경우 새로운 데이터만 저장

        else:
            updated_data = new_data  # 기존 데이터가 없을 경우 새로 생성
            st.success("✅ 기존 데이터 없음, 새 파일 생성")

        # ✅ CSV 저장
        updated_data.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        st.success("✅ 데이터 저장 완료!")

    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

# ✅ 기존 데이터 로드 함수
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", on_bad_lines="skip")

            # ✅ CSV 파일이 비어있는 경우
            if df.empty:
                st.warning("⚠️ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
                return pd.DataFrame(columns=EXPECTED_COLUMNS)

            # ✅ 컬럼 체크 및 자동 수정
            for col in EXPECTED_COLUMNS:
                if col not in df.columns:
                    df[col] = ""

            st.success("✅ 기존 데이터 로드 완료")  
            return df[EXPECTED_COLUMNS]  # ✅ 올바른 컬럼 구조 유지

        else:
            st.warning("⚠️ 저장된 데이터가 없습니다. 데이터를 분석한 후 다시 확인하세요.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)


# 예시: 이미지 업로드 및 처리
uploaded_file = st.file_uploader("도마뱀 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지를 저장하고 경로 반환
    image_path, image_name = save_image(uploaded_file)
    
    if image_path:
        st.image(image_path, caption="업로드된 이미지", use_column_width=True)

        # 분석 결과 저장 예시 (여기서 모프, 사이즈, 가격 등의 값을 사용자로부터 입력받을 수 있음)
        species = st.text_input("도마뱀 품종을 입력하세요")
        confidence = st.slider("예측 신뢰도", 0, 100, 50)
        morph = st.text_input("모프를 입력하세요 (선택사항)")
        size = st.text_input("크기를 입력하세요 (선택사항)")
        price = st.text_input("가격을 입력하세요 (선택사항)")

        if st.button("결과 저장"):
            save_prediction(uploaded_file, species, confidence, morph, size, price)
