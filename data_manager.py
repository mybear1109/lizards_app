import os
import pandas as pd
import datetime
import streamlit as st

# ✅ 데이터 파일 경로 설정
DATA_PATH = "data/Lizards.csv"
IMAGE_FOLDER = "data/images/"  # 이미지 저장 폴더

# ✅ CSV 파일의 올바른 컬럼 구조
EXPECTED_COLUMNS = ["Date", "Image", "Image_Path", "Species", "Confidence"]

# ✅ 분석 결과 저장 함수 (이미지 경로 저장)
def save_prediction(image_file, species, confidence):
    """ 분석된 결과를 CSV 파일에 저장하는 함수 """
    
    try:
        # ✅ 저장 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        os.makedirs(IMAGE_FOLDER, exist_ok=True)

        # ✅ image_file이 스트링(파일명)인지 확인 후 처리
        if isinstance(image_file, str):
            image_name = image_file  # 문자열 파일명
            image_path = os.path.join(IMAGE_FOLDER, image_name)
        else:
            # ✅ 이미지 저장 경로 설정
            image_name = image_file.name
            image_path = os.path.join(IMAGE_FOLDER, image_name)

            # ✅ 파일을 실제로 저장
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        new_data = pd.DataFrame({
            "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "Image": [image_name],
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

