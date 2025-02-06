import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"  # 이미지 저장 폴더

# ✅ CSV 파일의 올바른 컬럼 구조
EXPECTED_COLUMNS = ["Date", "Image", "Image_Path", "Species", "Confidence"]

# ✅ 분석 결과 저장 함수 (이미지 경로 추가)
def save_prediction(image_file, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """

    try:
        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        os.makedirs(IMAGE_FOLDER, exist_ok=True)

        # ✅ 이미지 저장 경로 설정
        image_path = os.path.join(IMAGE_FOLDER, image_file.name)
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())

        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_file.name],
            "Image_Path": [image_path],  # ✅ 이미지 경로 저장
            "Species": [species],
            "Confidence": [confidence]
        })

        # ✅ 기존 데이터 확인 후 컬럼 체크
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 기존 데이터 컬럼 검사 및 자동 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]

            if missing_columns:
                st.warning(f"⚠️ CSV 파일의 일부 컬럼이 누락되었습니다. 자동 복구: {missing_columns}")
                for col in missing_columns:
                    existing_data[col] = None  # ✅ 누락된 컬럼 추가

            # ✅ 컬럼 정렬 후 데이터 저장
            existing_data = existing_data[EXPECTED_COLUMNS]
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # ✅ CSV 파일 저장
        updated_data.to_csv(DATA_PATH, index=False)
        st.success("✅ 데이터 저장 완료!")

    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

# ✅ 기존 데이터 로드 함수 (이미지 경로 포함)
def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)

            # ✅ CSV 파일이 비어있는 경우
            if df.empty:
                st.warning("⚠️ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
                return pd.DataFrame(columns=EXPECTED_COLUMNS)

            # ✅ 컬럼 체크 및 자동 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]

            if missing_columns:
                st.warning(f"⚠️ CSV 파일의 일부 컬럼이 누락되었습니다. 자동 복구: {missing_columns}")
                for col in missing_columns:
                    df[col] = None  # ✅ 누락된 컬럼 추가

            return df[EXPECTED_COLUMNS]  # ✅ 올바른 컬럼 구조 유지
        else:
            st.warning("⚠️ 저장된 데이터가 없습니다. 데이터를 분석한 후 다시 확인하세요.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
