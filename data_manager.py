import os
import pandas as pd
import datetime
from PIL import Image
import streamlit as st

# ✅ 데이터 및 이미지 저장 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"

# ✅ CSV 파일의 올바른 컬럼 구조
EXPECTED_COLUMNS = ["Date", "Image", "Size", "Species", "Confidence", "Morph", "Price"]

# ✅ 디렉토리 생성 함수
def ensure_directory_exists(directory):
    """ 경로가 존재하지 않으면 생성하는 함수 """
    os.makedirs(directory, exist_ok=True)

# ✅ 이미지 저장 함수
def save_image(image_file):
    """ 이미지를 'data/images/' 폴더에 저장하고 경로 및 파일명을 반환하는 함수 """
    try:
        ensure_directory_exists(IMAGE_FOLDER)

        # 이미지 파일명 생성 (유니크한 이름)
        image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # 이미지 저장
        image = Image.open(image_file)

        # 파일 형식 확인 (지원되는 이미지 형식인지)
        if image.format not in ['JPEG', 'PNG','JPG', 'BMP','webp']:
            st.error("❌ 지원되지 않는 이미지 형식입니다. (JPEG, PNG, BMP, WEBP 형식만 가능)")
            return None, None

        image.save(image_path)
        st.success(f"✅ 이미지가 성공적으로 저장되었습니다: {image_name}")

        return image_path, image_name

    except Exception as e:
        st.error(f"❌ 이미지 저장 중 오류 발생: {e}")
        return None, None

# ✅ 분석 데이터 저장 함수
def save_prediction(image_file, species, confidence, morph="", size="", price=""):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
        ensure_directory_exists(os.path.dirname(DATA_PATH))

        # ✅ `image_file`이 None 또는 문자열이면 처리 중단
        if image_file is None or isinstance(image_file, str):
            st.error("❌ 유효한 이미지 파일이 아닙니다. 이미지를 업로드해주세요.")
            return

        # ✅ 이미지 파일명 생성
        image_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{image_file.name}"
        image_path = os.path.join(IMAGE_FOLDER, image_name)

        # ✅ 새로운 데이터 생성
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

                # ✅ 기존 컬럼이 없으면 자동 생성
                for col in EXPECTED_COLUMNS:
                    if col not in existing_data.columns:
                        existing_data[col] = ""

                existing_data = existing_data[EXPECTED_COLUMNS]
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)

            except Exception as e:
                st.error(f"❌ 기존 데이터 읽기 오류: {e}")
                updated_data = new_data  # 기존 데이터가 깨진 경우 새로운 데이터만 저장

        else:
            updated_data = new_data  # 기존 데이터가 없을 경우 새 파일 생성

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

            # CSV 파일이 비어있는 경우
            if df.empty:
                st.warning("⚠️ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
                return pd.DataFrame(columns=EXPECTED_COLUMNS)

            # 기존 컬럼 체크 및 자동 수정
            for col in EXPECTED_COLUMNS:
                if col not in df.columns:
                    df[col] = ""

            return df[EXPECTED_COLUMNS]  # 올바른 컬럼 구조 유지

        else:
            st.warning("⚠️ 저장된 데이터가 없습니다. 데이터를 분석한 후 다시 확인하세요.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
