import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
EXPECTED_COLUMNS = ["Date", "Image", "Image_Path", "Species", "Confidence"]

def save_prediction(image_name, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
        # ✅ 디렉토리 확인 및 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # ✅ 새로운 데이터 생성
        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence],
            "Image_Path": [os.path.join("images", image_name)]  # 이미지 경로 추가
        })

        # ✅ 기존 데이터 로드
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 컬럼 체크 및 자동 수정
            if list(existing_data.columns) != EXPECTED_COLUMNS:
                missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]
                for col in missing_columns:
                    existing_data[col] = None
                existing_data = existing_data[EXPECTED_COLUMNS]

            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # ✅ CSV 저장
        updated_data.to_csv(DATA_PATH, index=False)
        st.success("✅ 데이터 저장 완료!")
    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

def load_existing_data():
    """ 기존 분석 데이터를 불러오는 함수 """
    try:
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)

            # ✅ 컬럼 체크 및 자동 수정
            if list(df.columns) != EXPECTED_COLUMNS:
                missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
                for col in missing_columns:
                    df[col] = None
                df = df[EXPECTED_COLUMNS]
            return df
        else:
            st.warning("⚠️ 저장된 데이터가 없습니다.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)
    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
