import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"

# ✅ CSV 파일의 올바른 컬럼 구조
EXPECTED_COLUMNS = ["Date", "Image", "Image_Path", "Species", "Confidence"]

def save_prediction(image_file, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # ✅ 이미지 파일명과 경로 저장
        image_name = image_file.name if hasattr(image_file, "name") else image_file
        image_path = f"data/images/{image_name}"

        # ✅ 새로운 데이터 생성
        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Image_Path": [image_path],
            "Species": [species],
            "Confidence": [confidence]
        })

        # ✅ 기존 데이터 로드 및 컬럼 정리
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 기존 컬럼과 기대하는 컬럼 비교하여 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]
            for col in missing_columns:
                existing_data[col] = None  # 누락된 컬럼 추가

            existing_data = existing_data[EXPECTED_COLUMNS]
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

            def save_prediction(image_name, species, confidence, morph):
                new_data = pd.DataFrame({
                "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Image": [image_name],
                "Species": [species],
                "Confidence": [confidence],
                "Morph": [morph]  # ✅ 모프 데이터 추가
            })


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

            # ✅ CSV 파일이 비어있는 경우
            if df.empty:
                st.warning("⚠️ 분석할 데이터가 없습니다. 이미지를 먼저 업로드하세요.")
                return pd.DataFrame(columns=EXPECTED_COLUMNS)

            # ✅ 컬럼 체크 및 자동 수정
            missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
            for col in missing_columns:
                df[col] = None  # 누락된 컬럼 추가

            return df[EXPECTED_COLUMNS]  # ✅ 올바른 컬럼 구조 유지
        else:
            st.warning("⚠️ 저장된 데이터가 없습니다. 데이터를 분석한 후 다시 확인하세요.")
            return pd.DataFrame(columns=EXPECTED_COLUMNS)

    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
