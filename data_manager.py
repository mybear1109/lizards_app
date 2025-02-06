import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"  # 이미지 저장 폴더

# ✅ CSV 파일의 올바른 컬럼 구조
EXPECTED_COLUMNS = ["Date", "Image", "Image_Path", "Species", "Confidence"]

def save_prediction(uploaded_file, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    try:
        # ✅ 파일 이름 확인 및 처리
        if hasattr(uploaded_file, "name"):  # 업로드된 파일 객체일 경우
            image_name = uploaded_file.name
        else:  # 문자열로 전달된 경우
            image_name = uploaded_file

        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # ✅ 새로운 데이터 생성
        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
            "Species": [species],
            "Confidence": [confidence]
        })

        # ✅ 기존 데이터 로드 및 저장
        if os.path.exists(DATA_PATH):
            existing_data = pd.read_csv(DATA_PATH)

            # ✅ 컬럼 정렬 및 누락된 컬럼 처리
            if list(existing_data.columns) != EXPECTED_COLUMNS:
                st.warning("⚠️ CSV 파일의 컬럼이 올바르지 않습니다. 자동 수정됩니다.")
                missing_columns = [col for col in EXPECTED_COLUMNS if col not in existing_data.columns]
                for col in missing_columns:
                    existing_data[col] = None  # 누락된 컬럼 추가
                existing_data = existing_data[EXPECTED_COLUMNS]

            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # ✅ CSV 저장
        updated_data.to_csv(DATA_PATH, index=False)
        st.success("✅ 데이터 저장 완료!")
    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류 발생: {e}")

